# Revisión actual de cobertura y Revisar

Además de las pruebas históricas reproducidas, la prueba nueva usa el backend real de Revisar y un cooldown simulado. Consulta [Resultados de las pruebas](RESULTADOS_PRUEBAS.md).

---

# PRUEBAS CANCELACION CODIGO — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

La lógica de confirmación de detención y recuperación previa se mantiene. La gestión de errores internos de motores y los reintentos del MOD conserva la cancelación y el cierre de tareas pendientes. Las mediciones anteriores de latencia son históricas; no se han repetido en Windows durante esta revisión.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Pruebas completas de cancelación

El alias trial_flat pertenece al arnés de pruebas; no es un módulo externo requerido por la aplicación.

```python
import asyncio
import json
import threading
import time
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
import trial_flat as f

Loop=f.LN_src_core_cancellation__InterruptibleLoop
Interrupted=f.LN_src_core_cancellation__TranslationInterrupted
Pipeline=f.LN_src_core_pipeline_orchestrator__TranslationPipeline
Engine=f.LN_src_core_translators_base__TranslationEngine
metrics={}

def run_stopper(ready,stop):
    def work():
        if ready.wait(5):
            metrics['last_stop']=time.perf_counter();stop()
    t=threading.Thread(target=work);t.start();return t

@pytest.fixture
def setup(tmp_path,monkeypatch):
    monkeypatch.setenv('LINGUANOVA_DATA_DIR',str(tmp_path/'data'))
    config=f.LN_src_utils_config__ConfigManager();config.app_settings.ui_language='es'
    config.translation_settings.target_language='spanish';config.translation_settings.source_language='en'
    project=tmp_path/'Game';game=project/'game';game.mkdir(parents=True)
    (game/'script.rpy').write_text('label start:\n    "The sailor read the old map before sunset."\n    return\n')
    manager=f.LN_src_core_translators_manager__TranslationManager(config_manager=config)
    pipe=Pipeline(config,manager);pipe.configure(str(project),'spanish',source_language='en',engine=Engine.GOOGLE)
    return pipe,manager

def test_inflight_request_cancelled_without_waiting_for_60s_timeout():
    stopped=threading.Event();ready=threading.Event();closed=[]
    loop=Loop(stopped.is_set);asyncio.set_event_loop(loop.raw_loop)
    async def slow():
        ready.set()
        try:await asyncio.sleep(60)
        finally:closed.append(True)
    stopper=run_stopper(ready,lambda:(stopped.set(),loop.cancel_active()))
    with pytest.raises(Interrupted):loop.run_until_complete(slow())
    delay=time.perf_counter()-metrics['last_stop'];metrics['request_cancel_seconds']=delay
    loop.close_with();stopper.join()
    assert delay<0.8;assert closed==[True]

def test_cooperative_children_all_cancelled_and_no_retry():
    stopped=threading.Event();ready=threading.Event();closed=[]
    loop=Loop(stopped.is_set);asyncio.set_event_loop(loop.raw_loop)
    async def child(i):
        try:
            if i==3:ready.set()
            await asyncio.sleep(60)
        finally:closed.append(i)
    async def batch():return await asyncio.gather(*(child(i) for i in range(4)))
    stopper=run_stopper(ready,lambda:(stopped.set(),loop.cancel_active()))
    with pytest.raises(Interrupted):loop.run_until_complete(batch())
    loop.close_with();stopper.join();assert sorted(closed)==[0,1,2,3]

def test_pre_cancel_does_not_start_or_leak_coroutine():
    loop=Loop(lambda:True);calls=[]
    async def request():calls.append(True)
    with pytest.raises(Interrupted):loop.run_until_complete(request())
    loop.close_with();assert not calls

def test_normal_result_and_real_error_still_propagate():
    loop=Loop(lambda:False);asyncio.set_event_loop(loop.raw_loop)
    async def answer():return 42
    async def error():raise ValueError('real engine failure')
    assert loop.run_until_complete(answer())==42
    with pytest.raises(ValueError,match='real engine failure'):loop.run_until_complete(error())
    loop.close_with()

def test_cancel_does_not_wait_for_sdk_executor_thread():
    stopped=threading.Event();ready=threading.Event();release=threading.Event()
    loop=Loop(stopped.is_set);asyncio.set_event_loop(loop.raw_loop)
    def sdk():ready.set();release.wait(5);return 'abandoned response'
    async def request():return await asyncio.to_thread(sdk)
    stopper=run_stopper(ready,lambda:(stopped.set(),loop.cancel_active()))
    try:
        with pytest.raises(Interrupted):loop.run_until_complete(request())
        loop.close_with();delay=time.perf_counter()-metrics['last_stop'];metrics['executor_cancel_seconds']=delay
        assert delay<0.8
    finally:release.set();stopper.join()

def test_cleanup_is_bounded_even_if_client_close_stalls():
    loop=Loop(lambda:True);started=time.perf_counter()
    async def close():await asyncio.sleep(60)
    loop.close_with(close());assert time.perf_counter()-started<0.8

def test_actual_primary_method_cancels_request_and_preserves_cache(setup):
    pipe,manager=setup;ready=threading.Event();cancelled=[];calls=[]
    async def translate(requests):
        calls.append(len(requests));ready.set()
        try:await asyncio.sleep(60)
        finally:cancelled.append(True)
    manager.translate_batch=translate
    entry=f.LN_src_core_tl_parser__TranslationEntry('The sailor read the old map before sunset.','',str(Path(pipe.project_path)/'game/script.rpy'),2,'dialogue')
    stopper=run_stopper(ready,pipe.stop)
    with pytest.raises(Interrupted):pipe._translate_entries([entry])
    delay=time.perf_counter()-metrics['last_stop'];metrics['primary_stop_seconds']=delay
    stopper.join();assert delay<0.8;assert calls==[1];assert cancelled==[True]
    assert pipe._translation_loop is None
    from_cache=f.LN_src_utils_path_manager__translation_cache_file(pipe.config,pipe.project_path,pipe.game_exe_path,pipe.target_language)
    assert Path(from_cache).exists()

def test_cancel_during_online_detection_closes_temporary_detector(setup,monkeypatch):
    pipe,manager=setup;pipe.source_language='auto';ready=threading.Event();closed=[]
    class Detector:
        async def detect_language(self,*args,**kwargs):ready.set();await asyncio.sleep(60)
        async def close_session(self):closed.append(True)
    monkeypatch.setattr(f,'LN_src_utils_lang_detect__detect_source_evidence',lambda *a,**kw:{'code':None})
    monkeypatch.setattr(f,'LN_src_core_pipeline_orchestrator__GoogleTranslator',lambda **kw:Detector())
    entry=f.LN_src_core_tl_parser__TranslationEntry('The sailor read the old map before sunset.','',str(Path(pipe.project_path)/'game/script.rpy'),2,'dialogue')
    stopper=run_stopper(ready,pipe.stop)
    with pytest.raises(Interrupted):pipe._translate_entries([entry])
    stopper.join();assert closed==[True];assert pipe._translation_loop is None

def test_single_click_acknowledged_and_duplicate_click_ignored():
    calls=[];notifications=[]
    pipe=NS(stop=lambda:calls.append(True))
    app=NS(_is_translating=True,pipeline=pipe,cancellationChanged=NS(emit=lambda:notifications.append(True)),
        _work_queue=NS(drop_pending=lambda pred:[]),logMessage=NS(emit=lambda *a:None),_t=lambda *a:'Stopping',pipeline_worker=None)
    cls=f.LN_src_backend_app_backend__AppBackend
    cls.stop_translation(app);cls.stop_translation(app)
    assert calls==[True];assert notifications==[True]
    getter=cls.__dict__['cancellationRequested'].fget
    assert getter(app)
    cls._reset_cancellation(app);assert not getter(app)

def test_callback_cancellation_interrupts_interface_retry_sleep():
    stopped=threading.Event();ready=threading.Event();loop=Loop(stopped.is_set)
    asyncio.set_event_loop(loop.raw_loop)
    async def backoff():ready.set();await asyncio.sleep(30)
    stopper=run_stopper(ready,stopped.set)
    with pytest.raises(Interrupted):loop.run_until_complete(backoff())
    delay=time.perf_counter()-metrics['last_stop'];metrics['backoff_cancel_seconds']=delay
    loop.close_with();stopper.join();assert delay<0.8

def test_write_cancel_latency_evidence():
    data={k:v for k,v in metrics.items() if k!='last_stop'}
    (Path(__file__).resolve().parent.parent.parent/'cancel_fix/latency.json').write_text(json.dumps(data,indent=2))

```