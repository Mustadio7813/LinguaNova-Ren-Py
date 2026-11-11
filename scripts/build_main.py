"""Build the Windows application from the standalone 1.5.5 source."""
from pathlib import Path
import os
import shutil
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from start import prepare,checked


def install_optimizer_dependencies(python, log):
    requirements = ROOT/'requirements-optimizer.txt'
    result = subprocess.run(
        [str(python), '-m', 'pip', 'install', '--only-binary', ':all:', '-r', str(requirements)],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding='utf-8', errors='replace'
    )
    with log.open('a', encoding='utf-8') as stream:
        stream.write('\n$ pip install optional optimizer dependencies\n' + result.stdout)
    if result.returncode:
        print('Aviso: algunas bibliotecas opcionales del optimizador no se instalaron; la compilación continúa.')


def bundle_ffmpeg(python, log):
    distribution = ROOT/'dist'/'LinguaNova'
    ffmpeg_dir = distribution/'ffmpeg'
    supplied = ROOT/'recursos'/'ffmpeg'/'ffmpeg.exe'
    license_file = supplied.parent/'LICENSE_ffmpeg.txt'
    if supplied.is_file() and license_file.is_file():
        ffmpeg_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(supplied, ffmpeg_dir/'ffmpeg.exe')
        shutil.copy2(license_file, ffmpeg_dir/'LICENSE_ffmpeg.txt')
        print('FFmpeg incluido desde recursos/ffmpeg.')
        return
    if supplied.is_file():
        print('Aviso: no se incluye FFmpeg desde recursos porque falta LICENSE_ffmpeg.txt.')

    try:
        checked(
            [str(python), str(ROOT/'LinguaNova_Traductor_RenPy.py'),
             '--directo', '--descargar-ffmpeg', str(ffmpeg_dir)],
            log, cwd=ROOT
        )
    except RuntimeError:
        print('Aviso: no se pudo descargar FFmpeg; la aplicación podrá ofrecerlo al usar el optimizador.')


def main():
    if os.name!='nt':raise RuntimeError('La distribución Windows debe compilarse en Windows.')
    if sys.version_info<(3,10):raise RuntimeError('Se necesita Python 3.10 o superior.')
    if struct.calcsize('P')*8!=64:raise RuntimeError('Para compilar esta distribución Windows se necesita Python de 64 bits.')
    python=prepare(ROOT)
    log=ROOT/'compilacion_error.log'
    install_optimizer_dependencies(python, log)
    checked([str(python),'-m','pip','install','PyInstaller>=6.12,<7'],log,cwd=ROOT)
    checked([str(python),'-m','PyInstaller','--noconfirm','--clean',str(ROOT/'LinguaNova.spec')],log,cwd=ROOT)
    bundle_ffmpeg(python, log)
    print('Distribuye toda la carpeta dist/LinguaNova. El destinatario no necesita Python ni pip.')
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        raise SystemExit(1)
