"""Prueba real de «Aligerar el juego» (Utilidades) en Qt sin pantalla.

Uso: python docs/PRUEBA_ALIGERAR_JUEGO.py [LinguaNova_Traductor_RenPy.py]

Crea un juego Ren'Py de prueba (imágenes, audio, vídeo, un .rpa, motor de
Linux), abre la aplicación real con un perfil temporal, entra en Utilidades y
usa la tarjeta como lo haría el usuario: Calcular ahorro y Crear copia
optimizada. Comprueba la copia, el informe, que el original no cambió y que la
tarjeta existe en los cinco idiomas de la interfaz. Requisitos: las dependencias
de LinguaNova, Pillow y ffmpeg en el PATH para generar el juego de prueba.
No usa Internet ni proveedores de traducción.
"""
import hashlib
import io
import json
import os
import pickle
import runpy
import shutil
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / 'LinguaNova_Traductor_RenPy.py'
WORK = Path(tempfile.mkdtemp(prefix='ln_aligerar_'))
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_QUICK_BACKEND'] = 'software'
os.environ['LINGUANOVA_DATA_DIR'] = str(WORK / 'perfil')


def make_game(root):
    from PIL import Image
    game = root / 'game'
    for sub in ('images', 'audio', 'movies', 'tl/spanish'):
        (game / sub).mkdir(parents=True, exist_ok=True)
    (root / 'lib' / 'py3-windows-x86_64').mkdir(parents=True)
    (root / 'lib' / 'py3-linux-x86_64').mkdir(parents=True)
    (root / 'lib' / 'py3-linux-x86_64' / 'lib.so').write_bytes(os.urandom(100000))
    (root / 'Juego.sh').write_text('#!/bin/sh\n')
    (root / 'Juego.exe').write_bytes(b'MZ')
    (game / 'script.rpy').write_text('label start:\n    "Hola"\n', encoding='utf-8')
    (game / 'tl' / 'spanish' / 'x.rpy').write_text('translate spanish strings:\n', encoding='utf-8')

    def picture(i):
        im = Image.linear_gradient('L').resize((480, 360)).convert('RGB')
        r, g, b = im.split()
        return Image.merge('RGB', (r, g.rotate(i * 30), Image.effect_noise((480, 360), 8 + i).convert('L')))
    for i in range(4):
        picture(i).save(game / 'images' / f'bg{i}.png')
        picture(i + 9).save(game / 'images' / f'f{i}.jpg', quality=98)
    run = lambda *a: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
    run('-f', 'lavfi', '-i', 'sine=frequency=440:duration=5', '-ac', '2', '-c:a', 'libvorbis', '-q:a', '8', str(game / 'audio' / 'm.ogg'))
    run('-f', 'lavfi', '-i', 'testsrc=size=1280x720:rate=60:duration=2', '-c:v', 'libvpx-vp9', '-b:v', '4M', str(game / 'movies' / 'op.webm'))
    files = {}
    for i in range(2):
        b = io.BytesIO()
        picture(i + 20).save(b, 'PNG')
        files[f'images/rpa{i}.png'] = b.getvalue()
    key, pos, body, index = 0xDEADBEEF, 34, b'', {}
    for name, content in files.items():
        index[name] = [(pos ^ key, len(content) ^ key, b'')]
        body += content
        pos += len(content)
    header = f'RPA-3.0 {pos:016x} {key:08x}\n'.encode()
    (game / 'archive.rpa').write_bytes(header + body + zlib.compress(pickle.dumps(index, protocol=2)))
    return game


def fingerprint(root):
    h = hashlib.sha256()
    for p in sorted(root.rglob('*')):
        if p.is_file():
            h.update(str(p.relative_to(root)).encode() + p.read_bytes())
    return h.hexdigest()


GAME_ROOT = WORK / 'Juego Prueba'
make_game(GAME_ROOT)
BEFORE = fingerprint(GAME_ROOT)
results = {'checks': [], 'warnings': []}

from PyQt6 import QtCore, QtQml  # noqa: E402
Original = QtQml.QQmlApplicationEngine


def wait(ms):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(ms, loop.quit)
    loop.exec()


class Engine(Original):
    def __init__(self, *a):
        super().__init__(*a)
        self.warnings.connect(lambda ws: results['warnings'].extend(w.toString() for w in ws))

    def load(self, url):
        super().load(url)
        QtCore.QTimer.singleShot(1500, self.run_tests)

    def ev(self, code):
        root = self.rootObjects()[0]
        expr = QtQml.QQmlExpression(QtQml.qmlContext(root), root, code)
        value, _undefined = expr.evaluate()
        if expr.hasError():
            raise RuntimeError(expr.error().toString())
        return value.toVariant() if hasattr(value, 'toVariant') else value

    def check(self, name, ok, detail=''):
        results['checks'].append({'prueba': name, 'ok': bool(ok), 'detalle': str(detail)[:400]})

    def wait_idle(self, seconds):
        for _ in range(int(seconds * 10)):
            wait(100)
            if not self.ev('optimizerBackend.busy'):
                return True
        return False

    def run_tests(self):
        try:
            root = self.rootObjects()[0]
            root.showNormal()
            root.setGeometry(0, 0, 1400, 900)
            self.ev('appBackend.advancedMode = true')
            self.ev('appBackend.setProjectPath("%s")' % str(GAME_ROOT).replace('\\', '/'))
            self.ev('navIndex = 3')
            wait(800)
            card = root.findChild(QtCore.QObject, 'optimizeGameCard')
            self.check('La tarjeta existe en Utilidades', card is not None)
            self.check('La tarjeta está visible y tiene tamaño',
                       card is not None and card.property('visible') and card.property('height') > 100,
                       card.property('height') if card else None)
            self.check('Botón Crear copia habilitado con un juego abierto',
                       root.findChild(QtCore.QObject, 'createOptimizedCopy').property('enabled'))
            if os.environ.get('LN_CAPTURA'):  # opcional: guarda una captura de Utilidades
                root.grabWindow().save(os.environ['LN_CAPTURA'])
            self.check('ffmpeg detectado', len(self.ev('optimizerBackend.ffmpegPath')) > 0, self.ev('optimizerBackend.ffmpegPath'))

            self.ev('optimizerBackend.estimate(1, false, true)')
            wait(200)
            self.check('Calcular ahorro arranca en segundo plano', self.ev('optimizerBackend.busy'))
            self.check('Calcular ahorro termina', self.wait_idle(180))
            status = self.ev('optimizerBackend.status')
            self.check('La estimación muestra antes → después', '→' in status, status)
            self.check('Calcular ahorro no crea carpetas', not (WORK / 'Juego Prueba_Optimizado').exists())

            parent = QtCore.QUrl.fromLocalFile(str(WORK)).toString()
            self.ev(f'optimizerBackend.optimize("{parent}", 1, true, true, true)')
            self.check('Crear copia termina', self.wait_idle(300))
            out = WORK / 'Juego Prueba_Optimizado'
            status = self.ev('optimizerBackend.status')
            self.check('La copia existe', (out / 'game').is_dir(), status)
            self.check('Informe junto a la copia', Path(str(out) + '_informe.txt').is_file())
            self.check('Los .rpa se extrajeron en la copia', (out / 'game' / 'images' / 'rpa0.png').is_file()
                       and not (out / 'game' / 'archive.rpa').exists())
            self.check('Motor de Linux quitado', not (out / 'lib' / 'py3-linux-x86_64').exists()
                       and (out / 'lib' / 'py3-windows-x86_64').exists())
            self.check('Traducciones conservadas en la copia', (out / 'game' / 'tl' / 'spanish' / 'x.rpy').is_file())
            self.check('Ajustes de poca RAM añadidos', (out / 'game' / 'zz_gama_baja.rpy').is_file())
            before = sum(p.stat().st_size for p in GAME_ROOT.rglob('*') if p.is_file())
            after = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
            self.check('La copia pesa menos', after < before, f'{before} -> {after}')
            self.check('El juego original no cambió', fingerprint(GAME_ROOT) == BEFORE)
            self.check('Botón Abrir copia disponible', len(self.ev('optimizerBackend.lastOutputPath')) > 0)

            # Detener: la copia a medias se borra.
            self.ev(f'optimizerBackend.optimize("{parent}", 2, false, false, false)')
            wait(300)
            self.ev('optimizerBackend.cancel()')
            self.check('Detener termina la tarea', self.wait_idle(60))
            self.check('Detener informa al usuario', len(self.ev('optimizerBackend.status')) > 0, self.ev('optimizerBackend.status'))
            self.check('Detener no deja copias a medias', not Path(str(out) + '.parcial').exists())
            self.check('Detener conserva la copia anterior completa', (out / 'game' / 'zz_gama_baja.rpy').is_file())

            expected = {'es': 'Aligerar el juego', 'en': 'Lighten the game', 'fr': 'Alléger le jeu',
                        'pt': 'Deixar o jogo mais leve', 'ru': 'Облегчить игру'}
            for code, text in expected.items():
                self.ev(f'appBackend.setUILanguage("{code}")')
                wait(300)
                title = self.ev('appBackend.getTextWithDefault("opt_title", "?")')
                button = root.findChild(QtCore.QObject, 'createOptimizedCopy').property('text')
                self.check(f'Tarjeta traducida ({code})', title == text and button != 'Create lighter copy' or code == 'en',
                           f'{title} | {button}')
            self.ev('appBackend.setUILanguage("es")')
            ours = [w for w in results['warnings'] if 'OptimizeGameCard' in w]
            self.check('Sin avisos QML de la tarjeta nueva', not ours, ours)
        except Exception as e:
            self.check('Error inesperado en la prueba', False, repr(e))
        finally:
            QtCore.QTimer.singleShot(0, QtCore.QCoreApplication.instance().quit)


QtQml.QQmlApplicationEngine = Engine
sys.argv = [str(TARGET), '--directo']
try:
    runpy.run_path(str(TARGET), run_name='__main__')
except SystemExit:
    pass
failed = [c for c in results['checks'] if not c['ok']]
print(json.dumps({'total': len(results['checks']), 'fallidas': len(failed), 'checks': results['checks'],
                  'avisos_qml_totales': len(results['warnings'])}, ensure_ascii=False, indent=1))
shutil.rmtree(WORK, ignore_errors=True)
raise SystemExit(1 if failed else 0)
