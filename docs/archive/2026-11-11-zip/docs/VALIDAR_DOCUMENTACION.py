"""Revisión 2026-11-11_ALIGERAR_JUEGO. Validación de documentación e integridad.
Uso: python docs/VALIDAR_DOCUMENTACION.py
Comprueba JSON, sintaxis de scripts, hash de la fuente y todos los archivos
incluidos en el manifiesto. El manifiesto se excluye a sí mismo, expresamente.
No ejecuta las pruebas históricas ni consume servicios de traducción.
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
 path=base/relative
 assert path.is_file(),relative
 assert path.stat().st_size==info['bytes'],relative
 assert hashlib.sha256(path.read_bytes()).hexdigest()==info['sha256'],relative
print('Documentación e integridad correctas:',len(list(docs.iterdir())),'archivos en docs;',len(manifest['files']),'archivos comprobados.')
