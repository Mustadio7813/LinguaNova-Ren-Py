# PRUEBAS DEEPL COMPILACION CODIGO — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conservaron las correcciones previas de DeepL y el aislamiento de claves de compilación. Sus referencias de configuración y proxies se verificaron con el resto de motores. Los resultados antiguos de esta área son históricos; no representan una nueva llamada con credenciales ni una nueva compilación de Windows. Consultar los registros actuales para las pruebas ejecutadas.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Pruebas de perfiles y compilación

Se usan datos ficticios y el alias de pruebas trial_flat. La aplicación no depende de un módulo con ese nombre.

```python
import ast
from pathlib import Path
import sys
import pytest
import trial_flat as f
ROOT=Path(__file__).resolve().parents[3]
PROGRAM=ROOT/'trial_delivery/LinguaNova_versión1.5.5_Prueba/LinguaNova_versión1.5.5_Prueba.py'
PACKAGE=PROGRAM.parent

def boot_profile():
    tree=ast.parse(PROGRAM.read_text());nodes=[]
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='LN_DEPENDENCIES' for t in node.targets):break
        nodes.append(node)
    scope={'__name__':'test_profile_only','__file__':str(PROGRAM)}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'profile-prefix','exec'),scope)

@pytest.mark.parametrize('frozen,name',[(False,'Prueba_1.5.5'),(True,'Prueba_1.5.5_Compilado')])
def test_source_and_compiled_default_profiles_are_separate(tmp_path,monkeypatch,frozen,name):
    monkeypatch.delenv('LINGUANOVA_DATA_DIR',raising=False);monkeypatch.setenv('APPDATA',str(tmp_path))
    monkeypatch.setattr(sys,'frozen',frozen,raising=False)
    boot_profile()
    import os
    assert Path(os.environ['LINGUANOVA_DATA_DIR'])==tmp_path/'LinguaNova'/name

def test_compiled_profile_does_not_load_key_saved_while_testing_py(tmp_path,monkeypatch):
    import os
    monkeypatch.setenv('APPDATA',str(tmp_path));monkeypatch.delenv('LINGUANOVA_DATA_DIR',raising=False)
    monkeypatch.setattr(sys,'frozen',False,raising=False);boot_profile()
    source=f.LN_src_utils_config__ConfigManager();source.api_keys.deepl_api_key='UNIT_TEST_DUMMY_KEY_NOT_A_REAL_API:fx';assert source.save_config()
    source_path=source.config_file
    monkeypatch.delenv('LINGUANOVA_DATA_DIR');monkeypatch.setattr(sys,'frozen',True,raising=False);boot_profile()
    compiled=f.LN_src_utils_config__ConfigManager()
    assert compiled.config_file!=source_path
    assert not compiled.api_keys.deepl_api_key
    assert source_path.exists()
    assert 'UNIT_TEST_DUMMY_KEY_NOT_A_REAL_API' not in PROGRAM.read_text()

def test_explicit_data_override_remains_explicit(tmp_path,monkeypatch):
    monkeypatch.setenv('LINGUANOVA_DATA_DIR',str(tmp_path/'override'))
    monkeypatch.setattr(sys,'frozen',True,raising=False);boot_profile()
    import os
    assert os.environ['LINGUANOVA_DATA_DIR']==str(tmp_path/'override')

def test_compiler_bat_is_standalone_and_packages_only_code():
    bat=(PACKAGE/'COMPILAR_PRUEBA.bat').read_text(encoding='utf-8')
    assert 'INICIAR_PRUEBA.bat' not in bat
    assert 'LinguaNova_versión1.5.5_Prueba.py' in bat
    assert '--preparar' in bat and '--clean' in bat and '--onedir' in bat
    assert '--specpath' in bat and '--workpath' in bat
    assert '--add-data' not in bat and '--add-binary' not in bat
    assert 'set "LINGUANOVA_DATA_DIR="' in bat
    assert ' --distpath ' in bat
    assert 'api_keys.' not in bat
    assert not list(PACKAGE.glob('config.json'))

```

## Prueba de interfaz

```python
from pathlib import Path
import os,sys,importlib.util,json,tempfile
BASE=Path(__file__).resolve().parent
path=Path(sys.argv[1]).resolve()
expected='--fixed' in sys.argv
os.environ['LINGUANOVA_DATA_DIR']=tempfile.mkdtemp(prefix='deepl-ui-test-')
os.environ['QT_QPA_PLATFORM']='offscreen';os.environ['QT_QUICK_BACKEND']='software'
spec=importlib.util.spec_from_file_location('deepl_probe',path);f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QUrl,QObject,QPointF,QMetaObject,QEvent,QCoreApplication
from PyQt6.QtTest import QTest
from PyQt6.QtQuick import QQuickItem,QQuickWindow
from PyQt6 import sip
app=QApplication.instance() or QApplication([]);b=f.LN_src_backend_app_backend__AppBackend(parent=app)
python_errors=[]
def report_error(*args):
    import traceback
    python_errors.append(str(args[1]));traceback.print_exception(*args,file=sys.stderr)
sys.excepthook=report_error
e=QQmlApplicationEngine(app);backends=[]
for name,cls in [('appBackend',None),('editorBackend',f.LN_src_backend_editor_backend__EditorBackend),('dashboardBackend',f.LN_src_backend_dashboard_backend__DashboardBackend),('sharingBackend',f.LN_src_backend_sharing_backend__SharingBackend),('gameModBackend',f.LN_src_backend_game_mod_backend__GameModBackend)]:
 o=b if cls is None else cls(b,parent=app);backends.append(o);e.rootContext().setContextProperty(name,o)
e.addImportPath('qrc:/linguanova/src/gui/qml');e.load(QUrl('qrc:/linguanova/src/gui/qml/Main.qml'));assert e.rootObjects()
root=e.rootObjects()[0];root.setWidth(1366);root.setHeight(768);root.show()
b.setUILanguage('es');b.setSelectedEngine('deepl');b.refreshUI();QTest.qWait(400)
field=card=None
for candidate in root.findChildren(QObject,'deeplKeyField'):
 current=candidate
 while current is not None:
  if current.property('isAiEngine') is not None:
   field,card=candidate,current;break
  current=current.parentItem() if hasattr(current,'parentItem') else current.parent()
 if card is not None:break
assert card is not None
save=next(x for x in card.findChildren(QObject,'deeplKeySave'))
delete=next(x for x in card.findChildren(QObject,'deeplKeyDelete'))
def bounds(item):
 at=item.mapToItem(card,QPointF(0,0))
 return {'x':at.x(),'y':at.y(),'width':item.width(),'height':item.height(),'visible':item.isVisible(),
         'inside':at.y()>=0 and at.y()+item.height()<=card.height()+1 and at.x()>=0 and at.x()+item.width()<=card.width()+1}
initial={'card_height':card.height(),'card_width':card.width(),'input':bounds(field),'save':bounds(save),'delete':bounds(delete)}
(BASE/('after.json' if expected else 'before.json')).write_text(json.dumps(initial,indent=2))
if expected:
 assert all(initial[k]['inside'] and initial[k]['visible'] for k in ('input','save','delete')),initial
 layout_checks=[]
 for width,height in [(1366,768),(1024,720)]:
  root.setWidth(width);root.setHeight(height)
  for advanced in (False,True):
   b.advancedMode=advanced
   for locale in ('es','en','fr','pt','ru'):
    b.setUILanguage(locale);QTest.qWait(260)
    for item in [field,save,delete]:assert bounds(item)['inside'] and item.isVisible(),(width,height,advanced,locale,bounds(item),card.height())
    layout_checks.append([width,height,advanced,locale,card.height()])
 assert not b.hasDeeplKey and not save.property('enabled') and not delete.property('enabled')
 # Dummy keys: no API validation and no requests to DeepL are performed.
 key1='00000000-0000-0000-0000-000000000001:fx'
 key2='00000000-0000-0000-0000-000000000002:fx'
 field.setProperty('text',key1);app.processEvents();assert save.property('enabled')
 QMetaObject.invokeMethod(save,'clicked');app.processEvents()
 assert b.hasDeeplKey and field.property('text')=='' and delete.property('enabled')
 assert f.LN_src_utils_config__ConfigManager().api_keys.deepl_api_key==key1
 field.setProperty('text',key2);app.processEvents();QMetaObject.invokeMethod(save,'clicked');app.processEvents()
 assert f.LN_src_utils_config__ConfigManager().api_keys.deepl_api_key==key2
 assert key2 not in b.deeplKeyHint
 QMetaObject.invokeMethod(delete,'clicked');app.processEvents()
 assert not b.hasDeeplKey and not delete.property('enabled')
 assert f.LN_src_utils_config__ConfigManager().api_keys.deepl_api_key==''
 # Preserve the exact previous layout for unrelated engines.
 b.setSelectedEngine('google');b.refreshUI();QTest.qWait(280);assert abs(card.height()-135)<1
 b.setSelectedEngine('gemini');b.refreshUI();QTest.qWait(280);assert abs(card.height()-228)<1
 assert not python_errors,python_errors
 (BASE/'result.json').write_text(json.dumps({'layout_checks':len(layout_checks),'save_replace_delete_persisted':True,'other_engine_heights_unchanged':True,'python_errors':python_errors}))
b.shutdown();sip.delete(e);QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)
print(initial,flush=True)

```
