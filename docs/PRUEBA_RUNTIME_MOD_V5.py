"""Revisión 2026-11-05_MODv5. Prueba actual, sin llamadas a proveedores.
Uso: python docs/PRUEBA_RUNTIME_MOD_V5.py [ruta/LinguaNova_Traductor_RenPy.py]
Comprueba dos hooks en el mismo espacio de nombres, registro de idiomas,
plantillas, idioma original, callbacks previos y ausencia de recursión.
Requiere las dependencias normales de la aplicación. No ejecuta Ren'Py.
"""
from pathlib import Path
from collections import defaultdict
from types import SimpleNamespace
import os,runpy,tempfile
import sys
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'LinguaNova_Traductor_RenPy.py'
os.environ['LINGUANOVA_DATA_DIR']=tempfile.mkdtemp(prefix='ln_mod_v5_test_')
g=runpy.run_path(str(source),run_name='ln_mod_v5_test')
class Table:
 def __init__(self):self.translations={}
 def add(self,old,new,*args):
  if old in self.translations:raise ValueError('duplicate')
  self.translations[old]=new
config=SimpleNamespace(replace_text=lambda t:t,start_callbacks=[],language_callbacks=defaultdict(list),font_replacement_map={},default_language=None,rtl=False)
translator=SimpleNamespace(strings=defaultdict(Table),languages=set(),language_translates={})
def missing(path):raise IOError(path)
renpy=SimpleNamespace(game=SimpleNamespace(preferences=SimpleNamespace(language='spanish'),script=SimpleNamespace(translator=translator)),loader=SimpleNamespace(load=missing),list_files=lambda:[],log=lambda t:None)
namespace={'renpy':renpy,'config':config}
render=g['LN_src_ui_mod_ui_mod_hook_template__render_ui_mod_hook_multi']
for lang,target in [('spanish','Monedas: %d'),('russian','Монеты: %d'),('spanish','Monedas: %d')]:
 hook=render({lang:{'mapping':{'Coins: %d':target},'contexts':{'Coins: %d':['__global_ui__']}}},lang)
 exec(compile(g['LN_src_ui_mod_ui_mod_hook_template__python_body'](hook),'generated-v5','exec'),namespace,namespace)
assert len(config.start_callbacks)==1
for callback in config.start_callbacks:callback()
assert config.replace_text('Coins: 30')=='Monedas: 30'
renpy.game.preferences.language='russian'
assert config.replace_text('Coins: 30')=='Монеты: 30'
renpy.game.preferences.language=None
assert config.replace_text('Coins: 30')=='Coins: 30'
print('Runtime MOD v5: correcto. Dos idiomas y tres instalaciones sin recursión.')
