"""Validate the integrated documentation and retained delivery artifacts.
Uso: python docs/VALIDAR_DOCUMENTACION.py
Comprueba JSON, sintaxis de scripts, hash de la fuente y todos los archivos
incluidos en el manifiesto vigente. La copia original del manifiesto se
conserva en docs/archive/2026-11-11-zip/; los archivos históricos no presentes
en la raíz se validan desde ese archivo. El manifiesto se excluye a sí mismo.
No ejecuta pruebas históricas ni consume servicios de traducción.
"""
from pathlib import Path
import ast,json,hashlib
base=Path(__file__).resolve().parents[1];docs=base/'docs'
manifest=json.loads((docs/'MANIFIESTO_PRUEBA.json').read_text(encoding='utf-8'))
source=base/'LinguaNova_Traductor_RenPy.py'
assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['source_sha256']
for path in docs.iterdir():
 if path.suffix=='.json':json.loads(path.read_text(encoding='utf-8-sig'))
 elif path.suffix=='.py':compile(path.read_text(encoding='utf-8-sig'),str(path),'exec')
for relative,info in manifest['files'].items():
 candidates=(base/relative,docs/'archive'/'2026-11-11-zip'/relative)
 if not any(path.is_file()
            and path.stat().st_size==info['bytes']
            and hashlib.sha256(path.read_bytes()).hexdigest()==info['sha256']
            for path in candidates):
  raise AssertionError(f'No se encontró una copia íntegra de {relative}')
print('Documentación e integridad correctas:',len(list(docs.iterdir())),'archivos en docs;',len(manifest['files']),'archivos comprobados.')
