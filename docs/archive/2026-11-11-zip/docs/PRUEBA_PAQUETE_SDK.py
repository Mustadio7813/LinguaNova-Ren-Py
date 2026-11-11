"Revisión documental 2026-11-05_MODv5. Herramienta histórica conservada.\nEste documento se ha revisado en el contexto de la fuente actual: título «Traductor de Ren'Py», correcciones previas conservadas, runtime del MOD v5 y migración transaccional de scripts propios. Sus afirmaciones antiguas de pruebas, rutas o estructura se conservan como antecedentes identificados, no como evidencia de esta entrega. El estado completo y las limitaciones están en la guía y los resultados actuales.\nConsultar GUIA_COMPLETA.md y las pruebas actuales. No se afirma haber ejecutado esta herramienta con sus requisitos externos en esta revisión.\n"
import os, sys, runpy, tempfile, zipfile
from pathlib import Path
os.environ["LINGUANOVA_DATA_DIR"] = tempfile.mkdtemp()
g = runpy.run_path(sys.argv[1], run_name="ln_test")
root = Path(tempfile.mkdtemp()) / "Juego"; game = root / "game"
(game / "tl/spanish").mkdir(parents=True); (game / "tl/french").mkdir(parents=True)
(root / "J.exe").write_text("x")
# Archivo generado por el SDK de Ren'Py (sin marca) que LinguaNova tradujo en su sitio
(game / "tl/spanish/script.rpy").write_text('# TODO: Translation updated at 2026-11-05 10:00\n\n# game/script.rpy:3\ntranslate spanish start_1:\n\n    # e "Hello"\n    e "Hola"\n', encoding="utf-8")
(game / "tl/.diagnostics/spanish").mkdir(parents=True); (game / "tl/.diagnostics/spanish/coverage_by_category.json").write_text("{}")
(game / "tl/french/script.rpy").write_text('translate french start_1:\n    e "Bonjour"\n', encoding="utf-8")  # oficial
r = g["LN_src_core_sharing__build_package"](str(root), str(root.parent / "p.zip"))
print("idiomas:", r.languages, "| fuera:", r.skipped_languages)
print([n for n in zipfile.ZipFile(root.parent / "p.zip").namelist() if n.startswith("game/")])
