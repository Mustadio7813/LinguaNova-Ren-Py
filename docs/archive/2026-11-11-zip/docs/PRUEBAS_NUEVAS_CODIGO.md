# Revisión actual de cobertura y Revisar

La prueba nueva de cobertura, recuperación y Revisar está en [PRUEBA_COBERTURA_RECUPERACION_REVISAR.py](PRUEBA_COBERTURA_RECUPERACION_REVISAR.py). Consulta [Resultados de las pruebas](RESULTADOS_PRUEBAS.md).

---

# PRUEBAS NUEVAS CODIGO — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Este documento se ha revisado en el contexto de la fuente actual: título «Traductor de Ren'Py», correcciones previas conservadas, runtime del MOD v5 y migración transaccional de scripts propios. Sus afirmaciones antiguas de pruebas, rutas o estructura se conservan como antecedentes identificados, no como evidencia de esta entrega. El estado completo y las limitaciones están en la guía y los resultados actuales.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Código íntegro de las pruebas nuevas

Estas pruebas importan el .py mediante el alias de pruebas trial_flat; ese alias solo existe en el arnés de verificación, no en la aplicación.

```python
import asyncio
import json
import os
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
import trial_flat as f

Operation=f.LN_src_core_trial_workflow__TrialOperation
Blocked=f.LN_src_core_trial_workflow__TrialBlocked
Cancelled=f.LN_src_core_trial_workflow__TrialCancelled
prepared=f.LN_src_core_trial_workflow__prepared_record
restore=f.LN_src_core_trial_workflow__restore_previous
repair=f.LN_src_core_trial_integrity__deduplicate_strings
read_defs=f.LN_src_core_trial_integrity__string_definitions
Pipeline=f.LN_src_core_pipeline_orchestrator__TranslationPipeline
Result=f.LN_src_core_pipeline_base__PipelineResult
Stage=f.LN_src_core_pipeline_base__PipelineStage
Engine=f.LN_src_core_translators_base__TranslationEngine

@pytest.fixture
def config(tmp_path,monkeypatch):
    monkeypatch.setenv('LINGUANOVA_DATA_DIR',str(tmp_path/'data'))
    c=f.LN_src_utils_config__ConfigManager()
    c.app_settings.ui_language='es';c.translation_settings.target_language='spanish'
    c.translation_settings.source_language='en'
    return c

@pytest.fixture
def game(tmp_path):
    p=tmp_path/'Juego prueba';g=p/'game';g.mkdir(parents=True)
    (g/'script.rpy').write_text('label start:\n    "The sailor read the old map before sunset."\n    return\n')
    (p/'Juego.sh').write_text('#!/bin/sh\nexit 0\n')
    return p,g

def output(g,content='translate spanish strings:\n    old "Hello"\n    new "Hola"\n'):
    p=g/'tl/spanish/common.rpy';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content);return p

def op(config,game,cancel=lambda:False):
    p,g=game;return Operation(config,p,g,'spanish','google',cancel)

def result(success=True,**stats):
    return Result(success,'done',Stage.COMPLETED,stats=stats,output_path='output')

def test_ready_requires_output_and_hashes(config,game):
    p,g=game;o=op(config,game);o.begin();out=output(g)
    try:r=o.finish(result());assert r.stats['prepared']
    finally:o.close()
    assert prepared(config,p,'spanish')
    out.write_text(out.read_text()+'# edited\n')
    assert not prepared(config,p,'spanish')

def test_no_outputs_never_ready(config,game):
    o=op(config,game);o.begin()
    try:assert not o.finish(result()).stats['prepared']
    finally:o.close()

def test_source_change_revokes_launch(config,game):
    p,g=game;o=op(config,game);o.begin();output(g);o.finish(result());o.close()
    (g/'script.rpy').write_text('label start:\n    "Changed source."\n')
    assert not prepared(config,p,'spanish')

def test_language_isolation(config,game):
    p,g=game;o=op(config,game);o.begin();output(g);o.finish(result());o.close()
    assert not prepared(config,p,'french')

def test_lock_prevents_concurrent_language(config,game):
    p,g=game;o=op(config,game);o.begin()
    try:
        with pytest.raises(Blocked):Operation(config,p,g,'french','bing').begin()
    finally:o.close()

def test_bad_lock_not_silently_removed(config,game):
    o=op(config,game);o.folder.mkdir(parents=True);o.lock.write_text('not json')
    with pytest.raises(Blocked):o.begin()
    assert o.lock.exists()

def test_release_cannot_delete_another_owners_lock(config,game):
    o=op(config,game);o.begin();o.lock.write_text(json.dumps({'pid':os.getpid(),'token':'other'}));o.close()
    assert o.lock.exists()

def test_cancel_before_inventory_keeps_recoverable_state(config,game):
    o=op(config,game,lambda:True)
    try:
        with pytest.raises(Cancelled):o.begin()
    finally:o.close()
    assert not o.lock.exists()

def test_user_corrections_are_file_protected(config,game):
    p,g=game;o=op(config,game);o.begin();out=output(g);o.finish(result());o.close()
    changed=b'\xef\xbb\xbftranslate spanish strings:\r\n    old "Hello"\r\n    new "Hola, amigo"\r\n'
    out.write_bytes(changed)
    n=op(config,game);n.begin();out.write_text('overwritten by simulated run')
    try:r=n.finish(result());assert r.stats['partial'];assert out.read_bytes()==changed
    finally:n.close()
    assert n.data['protected']

def test_restore_is_verified_and_preserves_prior_bytes(config,game):
    p,g=game;out=output(g);prior=out.read_bytes();o=op(config,game);o.begin()
    out.write_text(out.read_text().replace('Hola','Buenas'));o.finish(result());o.close()
    assert restore(config,p,'spanish')>=1
    assert out.read_bytes()==prior
    assert not prepared(config,p,'spanish')

def test_restore_refuses_later_human_edits(config,game):
    p,g=game;o=op(config,game);o.begin();out=output(g);o.finish(result());o.close();out.write_text('human correction')
    with pytest.raises(Blocked):restore(config,p,'spanish')
    assert out.read_text()=='human correction'

def test_symlink_and_traversal_rejected(config,game,tmp_path):
    _,g=game
    with pytest.raises(Blocked):f.LN_src_core_trial_workflow__checked_game_path(g,'../outside')
    (g/'alias').symlink_to(tmp_path,target_is_directory=True)
    with pytest.raises(Blocked):f.LN_src_core_trial_workflow__checked_game_path(g,'alias/file')

@pytest.mark.parametrize('second',['Haz clic para reproducir el vídeo.','Pulsa para reproducir el vídeo.'])
def test_reported_valley_awakening_duplicate_and_stale_rpyc(config,game,second):
    _,g=game;text='Click to play the video.'
    first=output(g,f'translate spanish strings:\n    old "{text}"\n    new "Haz clic para reproducir el vídeo."\n')
    engine=g/'tl/spanish/_engine/common/000statements.rpy';engine.parent.mkdir(parents=True)
    engine.write_text(f'translate spanish strings:\n    old "{text}"\n    new "{second}"\n')
    compiled=engine.with_suffix('.rpyc');compiled.write_bytes(b'old compiled registrations')
    original_script=(g/'script.rpy').read_bytes()
    o=op(config,game);o.begin()
    try:
        changes=repair(o);assert len(changes)==1
        assert sum(len(read_defs(p,'spanish')[1]) for p in [first,engine])==1
        assert not compiled.exists()
        assert repair(o)==[]
        assert (g/'script.rpy').read_bytes()==original_script
        assert o.data['integrity_backups']
    finally:o.close()

def test_same_text_other_language_and_context_not_duplicate(config,game):
    _,g=game;path=output(g,'translate spanish strings:\n    old "Open"\n    new "Abrir"\n    old "Open{#state}"\n    new "Abierto"\n\ntranslate french strings:\n    old "Open"\n    new "Ouvrir"\n')
    o=op(config,game);o.begin()
    try:assert not repair(o);assert len(read_defs(path,'spanish')[1])==2
    finally:o.close()

def test_escaped_and_multiline_literals(config,game):
    _,g=game;path=output(g,'translate spanish strings:\n    old "Click \\\"play\\\""\n    new "Pulsa reproducir"\n    old "Click \\\"play\\\""\n    new "Pulsa reproducir"\n    old """Line one\nline two"""\n    new "Dos líneas"\n')
    o=op(config,game);o.begin()
    try:assert len(repair(o))==1;assert len(read_defs(path,'spanish')[1])==2
    finally:o.close()

def test_no_rewrite_outside_target_tl(config,game):
    _,g=game
    author=g/'original_translation.rpy';author.write_text('translate spanish strings:\n    old "Hello"\n    new "Hola del autor"\n')
    output(g)
    o=op(config,game);o.begin();before=author.read_bytes()
    try:assert len(repair(o))==1;assert author.read_bytes()==before
    finally:o.close()

def test_pre_cancel_emits_exactly_once(config,game):
    p,_=game;pipe=Pipeline(config,NS());pipe.configure(str(p),'spanish',source_language='en');pipe.stop()
    results=[];pipe.finished.connect(results.append);pipe.run()
    assert len(results)==1;assert results[0].stats['stopped'];assert not pipe.is_running

def test_invalid_game_never_calls_primary(config,tmp_path):
    folder=tmp_path/'invalid';folder.mkdir();pipe=Pipeline(config,NS());pipe.configure(str(folder),'spanish')
    pipe._run_pipeline=lambda:pytest.fail('must not run');results=[];pipe.finished.connect(results.append);pipe.run()
    assert len(results)==1;assert not results[0].success

def test_auto_flow_calls_interface_and_never_installs_panel(config,game,monkeypatch):
    p,g=game;pipe=Pipeline(config,NS());pipe.configure(str(p),'spanish',source_language='en')
    def primary():
        output(g);return result(total=1,translated=1)
    pipe._run_pipeline=primary;called=[]
    def interface(pipeline,operation):
        called.append(True);return NS(candidates=1,translated=1,pending=0,report_path='',success=True,partial=False,message_key='',message='')
    monkeypatch.setattr(f,'LN_src_core_trial_workflow__prepare_interface',interface)
    monkeypatch.setattr(f,'LN_src_core_delivery__install',lambda *a:None)
    monkeypatch.setattr(f,'LN_src_game_mod__install',lambda *a,**kw:pytest.fail('optional panel must not be installed'))
    results=[];pipe.finished.connect(results.append);pipe.run()
    assert called==[True];assert len(results)==1;assert results[0].success
    assert results[0].stats['prepared'];assert prepared(config,p,'spanish')

def test_interface_pending_is_partial_but_valid(config,game,monkeypatch):
    p,g=game;pipe=Pipeline(config,NS());pipe.configure(str(p),'spanish',source_language='en')
    def primary():output(g);return result(total=1,translated=1)
    pipe._run_pipeline=primary
    monkeypatch.setattr(f,'LN_src_core_trial_workflow__prepare_interface',lambda *a:NS(candidates=3,translated=1,pending=2,report_path='',success=True,partial=True,message_key='',message=''))
    monkeypatch.setattr(f,'LN_src_core_delivery__install',lambda *a:None)
    results=[];pipe.finished.connect(results.append);pipe.run()
    assert results[0].stats['partial'];assert results[0].stats['prepared']

def test_bad_primary_output_blocks_ready_and_interface(config,game,monkeypatch):
    p,g=game;pipe=Pipeline(config,NS());pipe.configure(str(p),'spanish')
    def primary():output(g);return result(syntax_issues=1)
    pipe._run_pipeline=primary
    monkeypatch.setattr(f,'LN_src_core_trial_workflow__prepare_interface',lambda *a:pytest.fail('must not run interface'))
    monkeypatch.setattr(f,'LN_src_core_delivery__install',lambda *a:None)
    results=[];pipe.finished.connect(results.append);pipe.run()
    assert not results[0].success;assert not results[0].stats['prepared']

def test_cooperative_interface_request_is_cancelled_and_drained():
    cancelled=[]
    async def request():
        try:await asyncio.sleep(10)
        finally:cancelled.append(True)
    async def exercise():
        calls=0
        def stop():
            nonlocal calls
            calls+=1;return calls>=2
        with pytest.raises(InterruptedError):await f.LN_src_ui_mod_generator___trial_await(request(),stop)
    asyncio.run(exercise());assert cancelled==[True]

def test_real_interface_generator_reuses_primary_translation_without_api(config,game,monkeypatch):
    p,g=game
    (g/'script.rpy').write_text('screen inventory():\n    textbutton "Open inventory" action NullAction()\n')
    output(g,'translate spanish strings:\n    old "Open inventory"\n    new "Abrir inventario"\n')
    class NoNetwork:
        async def translate_batch(self,requests):pytest.fail('existing primary translation must be reused')
    monkeypatch.setattr(f,'LN_src_ui_mod_generator__plan_fonts',lambda *a,**kw:({}, {'status':'not_needed'}))
    checkpoints=[]
    generated=f.LN_src_ui_mod_generator__generate_interface_mod(str(p),'en','spanish',Engine.GOOGLE,NoNetwork(),
        allow_identity_language=True,checkpoint=lambda entries:checkpoints.append(len(entries)))
    assert generated.success,generated.message
    assert generated.translated==1
    assert Path(generated.output_path).exists()
    assert checkpoints and checkpoints[-1]==1
    assert not (g/'zz_linguanova/mod.rpy').exists()

def test_generator_cancel_before_publish_leaves_no_interface_hook(config,game):
    p,g=game
    (g/'script.rpy').write_text('screen inventory():\n    textbutton "Open inventory" action NullAction()\n')
    with pytest.raises(InterruptedError):
        f.LN_src_ui_mod_generator__generate_interface_mod(str(p),'en','spanish',Engine.GOOGLE,NS(),
            cancel_requested=lambda:True)
    assert not list(g.glob('linguanova_mod_*_multilang.rpy'))

def test_launch_rechecks_after_canlaunch(config,game,monkeypatch):
    from PyQt6.QtCore import QObject,pyqtSignal
    p,g=game;o=op(config,game);o.begin();out=output(g);o.finish(result());o.close()
    class App(QObject):
        projectChanged=pyqtSignal(str);translationFinished=pyqtSignal(bool,str);logMessage=pyqtSignal(str,str)
        isTranslating=False;modRunning=False
        def __init__(self):super().__init__();self.config=config
        def _t(self,key,default='',**kw):return key
    app=App();dashboard=f.LN_src_backend_dashboard_backend__DashboardBackend(app)
    dashboard._info={'project_dir':str(p),'launcher':'Juego.sh'}
    assert dashboard.canLaunch
    out.write_text(out.read_text()+'# changed after button enabled\n')
    monkeypatch.setattr(f.LN_src_backend_dashboard_backend__subprocess,'Popen',lambda *a,**kw:pytest.fail('must not launch'))
    assert not dashboard.launchGame()

def test_launcher_ambiguity_requires_explicit_selection(game):
    p,g=game;(p/'Other.sh').write_text('#!/bin/sh\n')
    inspect=f.LN_src_core_project_inspector__inspect_project
    assert inspect(str(p)).launcher==''
    assert inspect(str(p/'Other.sh')).launcher=='Other.sh'

def test_duplicate_repair_wont_override_protected_file(config,game):
    p,g=game;out=output(g);o=op(config,game);o.begin();o.finish(result());o.close()
    out.write_text(out.read_text()+'\ntranslate spanish strings:\n    old "Hello"\n    new "Saludos"\n')
    n=op(config,game);n.begin();before=out.read_bytes()
    try:
        with pytest.raises(Blocked):repair(n)
        assert out.read_bytes()==before
    finally:n.close()

def test_malformed_json_cannot_be_ready(config,game):
    p,g=game;o=op(config,game);o.begin();out=output(g)
    (out.parent/'strings.json').write_text('{broken')
    try:
        with pytest.raises(ValueError):o.finish(result())
    finally:o.close()
    assert not prepared(config,p,'spanish')

def test_compiled_only_conflict_blocks_readiness_without_deletion(config,game,monkeypatch):
    p,g=game;out=output(g);orphan=out.parent/'orphan.rpyc';orphan.write_bytes(b'compiled-only input')
    monkeypatch.setattr(f,'LN_src_core_existing_translations__strings_from_compiled',lambda *a:{'Hello':'Hola'})
    o=op(config,game);o.begin()
    try:
        with pytest.raises(Blocked):repair(o)
        assert orphan.read_bytes()==b'compiled-only input'
    finally:o.close()

def test_restore_cannot_leave_orphan_compiled_output(config,game):
    p,g=game;o=op(config,game);o.begin();out=output(g);o.finish(result());o.close()
    compiled=out.with_suffix('.rpyc');compiled.write_bytes(b'compiled after running game')
    restore(config,p,'spanish')
    assert not out.exists();assert not compiled.exists()
    assert list(o.folder.glob('recovery_compiled/**/*.rpyc'))

```
