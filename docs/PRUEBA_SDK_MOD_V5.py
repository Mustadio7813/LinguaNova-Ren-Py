"""Revisión 2026-11-05_MODv5. Prueba real de hooks duplicados con un SDK.
Uso: python docs/PRUEBA_SDK_MOD_V5.py RUTA_SDK [ruta/LinguaNova_Traductor_RenPy.py]
Se recomienda el SDK oficial Ren'Py 7.4.4 para repetir la compatibilidad del caso.
Crea un proyecto temporal, ejecuta dos hooks y comprueba idiomas y textos.
En Linux usa SDL dummy y render software; no ejecuta el juego del usuario.
No necesita claves de proveedores y no descarga el SDK.
"""
from pathlib import Path
import os,sys,runpy,tempfile,subprocess,json
sdk=Path(sys.argv[1]).resolve()
source=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else Path(__file__).resolve().parents[1]/'LinguaNova_Traductor_RenPy.py'
project=Path(tempfile.mkdtemp(prefix='ln_sdk_v5_'));game=project/'game';game.mkdir()
os.environ['LINGUANOVA_DATA_DIR']=tempfile.mkdtemp(prefix='ln_sdk_config_')
g=runpy.run_path(str(source),run_name='ln_sdk_v5')
render=g['LN_src_ui_mod_ui_mod_hook_template__render_ui_mod_hook_multi']
for i,(language,word) in enumerate([('spanish','Monedas: %d'),('russian','Монеты: %d')]):
 (game/f'linguanova_mod_test_{i}_multilang.rpy').write_text(render({language:{'mapping':{'Coins: %d':word},'contexts':{}}},language),encoding='utf-8')
(game/'zz_verify.rpy').write_text('''define config.name = "LinguaNova SDK test"
init 999 python:
    def ln_qa_verify():
        import json
        renpy.game.preferences.language = 'spanish'
        assert config.replace_text('Coins: 30') == u'Monedas: 30'
        renpy.game.preferences.language = 'russian'
        assert config.replace_text('Coins: 30') == u'Монеты: 30'
        renpy.game.preferences.language = None
        assert config.replace_text('Coins: 30') == 'Coins: 30'
        with open(config.basedir + '/result.json', 'w') as stream:
            json.dump({'status':'OK','runtime':renpy.version()},stream)
        renpy.quit()
    config.start_callbacks.append(ln_qa_verify)
label start:
    return
''',encoding='utf-8')
env=os.environ.copy()
if os.name!='nt':env.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',RENPY_RENDERER='sw')
launcher=sdk/('renpy.exe' if os.name=='nt' else 'renpy.sh')
result=subprocess.run([str(launcher),str(project)],env=env,timeout=60)
if result.returncode:raise SystemExit(result.returncode)
proof=json.loads((project/'result.json').read_text())
assert proof['status']=='OK',proof
print(json.dumps(proof,ensure_ascii=False))
print('Proyecto de prueba:',project)
