# PRUEBAS NAVEGACION CODIGO — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conserva la navegación entre Traducción y MOD y el comportamiento previo del modo avanzado. La revisión actual modifica el título visible y el runtime generado; no sustituye esa lógica. Los resultados antiguos de navegación se conservan como antecedentes y se distinguen de la carga completa actual de la interfaz en Linux.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Código íntegro de las pruebas de navegación

El alias de pruebas `trial_flat` apunta al único archivo plano de esta entrega.

```python
"""Navigation regression: active translation -> MOD -> translation -> Stop."""
from types import SimpleNamespace
import pytest
import trial_flat as f
from PyQt6.QtCore import QObject,QMetaObject,QUrl,QCoreApplication,QEvent
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6 import sip

@pytest.mark.parametrize('advanced',[False,True])
def test_return_from_mod_while_translating_and_stop_stays_accessible(tmp_path,monkeypatch,advanced):
    monkeypatch.setenv('LINGUANOVA_DATA_DIR',str(tmp_path/'data'))
    app=QApplication.instance() or QApplication([])
    backend=f.LN_src_backend_app_backend__AppBackend(parent=app)
    engine=QQmlApplicationEngine(app);objects=[];stop_calls=[]
    try:
        for name,cls in [('appBackend',None),('editorBackend',f.LN_src_backend_editor_backend__EditorBackend),
                ('dashboardBackend',f.LN_src_backend_dashboard_backend__DashboardBackend),
                ('sharingBackend',f.LN_src_backend_sharing_backend__SharingBackend),
                ('gameModBackend',f.LN_src_backend_game_mod_backend__GameModBackend)]:
            obj=backend if cls is None else cls(backend,parent=app);objects.append(obj)
            engine.rootContext().setContextProperty(name,obj)
        engine.addImportPath('qrc:/linguanova/src/gui/qml')
        engine.load(QUrl('qrc:/linguanova/src/gui/qml/Main.qml'));assert engine.rootObjects()
        root=engine.rootObjects()[0];backend.advancedMode=advanced
        app.processEvents()
        nav={};pending=[root.contentItem()]
        while pending:
            item=pending.pop()
            index=item.property('pageIndex')
            if index in range(7):nav[index]=item
            pending.extend(item.childItems())
        assert set(nav)==set(range(7))
        pipeline=SimpleNamespace(stop=lambda:stop_calls.append(True))
        backend.pipeline=pipeline;backend._is_translating=True
        backend.translationStarted.emit();root.setProperty('isTranslating',True);root.setProperty('currentStage','translating')
        app.processEvents()
        assert nav[0].property('enabled') and nav[6].property('enabled')
        for index in (1,2,3,4,5):assert not nav[index].property('enabled')
        # Input-bearing cards stay locked: navigation alone must not edit the run.
        cards=[o for o in root.findChildren(QObject) if o.property('isAiEngine') is not None]
        assert cards and not cards[0].property('enabled')
        for _ in range(3):
            assert nav[6].property('enabled')
            QMetaObject.invokeMethod(nav[6],'clicked');app.processEvents();assert root.property('navIndex')==6
            assert nav[0].property('enabled')
            QMetaObject.invokeMethod(nav[0],'clicked');app.processEvents();assert root.property('navIndex')==0
            assert backend.isTranslating and backend.pipeline is pipeline and not stop_calls
        stop_button=root.findChild(QObject,'mainTranslateButton')
        assert stop_button is not None and stop_button.property('enabled')
        QMetaObject.invokeMethod(stop_button,'clicked');app.processEvents()
        assert stop_calls==[True] and backend.cancellationRequested
        assert not stop_button.property('enabled')
        backend._on_pipeline_finished(f.LN_src_core_pipeline_base__PipelineResult(False,'Stopped',
            f.LN_src_core_pipeline_base__PipelineStage.IDLE,stats={'stopped':True,'prepared':False}))
        app.processEvents()
        assert not backend.isTranslating and stop_button.property('enabled')
        assert all(nav[i].property('enabled') for i in range(7))
    finally:
        backend._is_translating=False
        backend.shutdown();sip.delete(engine)
        QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)

```
