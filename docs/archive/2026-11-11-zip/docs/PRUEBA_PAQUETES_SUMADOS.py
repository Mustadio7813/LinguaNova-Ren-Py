"Revisión documental 2026-11-05_MODv5. Herramienta histórica conservada.\nEste documento se ha revisado en el contexto de la fuente actual: título «Traductor de Ren'Py», correcciones previas conservadas, runtime del MOD v5 y migración transaccional de scripts propios. Sus afirmaciones antiguas de pruebas, rutas o estructura se conservan como antecedentes identificados, no como evidencia de esta entrega. El estado completo y las limitaciones están en la guía y los resultados actuales.\nConsultar GUIA_COMPLETA.md y las pruebas actuales. No se afirma haber ejecutado esta herramienta con sus requisitos externos en esta revisión.\n\nDescripción original:\nDos paquetes de LinguaNova copiados sobre el mismo juego: ¿se suman?\n\nUso: python probar_menu_dinamico.py RUTA/LinguaNova_Traductor_RenPy.py\n1. Crea dos copias del mismo juego, con una fuente que solo tiene letras latinas.\n2. En la copia A «traduce» al ruso (cirílico: la fuente no sirve) y en la B al español.\n3. Instala zz_linguanova en cada una y crea su paquete.\n4. Copia A y después B sobre un juego limpio (B reemplaza linguanova.rpy de A).\n5. Ejecuta el bloque init 999 de linguanova.rpy con un `renpy` simulado y comprueba\n   que el menú conoce los dos idiomas y que el ruso conserva su corrección de fuente.\n"
import json, os, runpy, shutil, sys, tempfile, textwrap, types, zipfile
from pathlib import Path

os.environ["LINGUANOVA_DATA_DIR"] = tempfile.mkdtemp()
g = runpy.run_path(sys.argv[1], run_name="ln_test")
from fontTools import subset

work = Path(tempfile.mkdtemp())
latin_font = work / "latin.ttf"
opts = subset.Options(); opts.unicodes = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180))
f = subset.load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", opts); s = subset.Subsetter(opts); s.populate(unicodes=opts.unicodes); s.subset(f); subset.save_font(f, str(latin_font), opts)

def make_game(name):
    root = work / name / "Mi Juego"
    (root / "game/fonts").mkdir(parents=True)
    (root / "MiJuego.exe").write_text("exe")
    (root / "game/script.rpy").write_text('define e = Character("Eileen")\nlabel start:\n    e "Hello, this is a long enough English sentence."\n', encoding="utf-8")
    shutil.copy(latin_font, root / "game/fonts/main.ttf")
    return root

marker = "# LinguaNova bounded translation output v1\n"
a = make_game("A"); (a / "game/tl/russian").mkdir(parents=True)
(a / "game/tl/russian/script.rpy").write_text(marker + 'translate russian start_1:\n    e "Привет, это достаточно длинное русское предложение."\n', encoding="utf-8")
b = make_game("B"); (b / "game/tl/spanish").mkdir(parents=True)
(b / "game/tl/spanish/script.rpy").write_text(marker + 'translate spanish start_1:\n    e "Hola, esta es una frase en español suficientemente larga."\n', encoding="utf-8")

install = g["LN_src_core_delivery__install"]; build = g["LN_src_core_sharing__build_package"]
packages = []
for root in (a, b):
    r = install(str(root / "game"), None)
    print(root.parent.name, "instalado: idiomas", r["languages"], "| fuentes a reemplazar", r["font_gaps"])
    print("   ", sorted(p.name for p in (root / "game/zz_linguanova/languages").iterdir()) if (root / "game/zz_linguanova/languages").is_dir() else "-")
    out = work / f"{root.parent.name}.zip"; build(str(root), str(out)); packages.append(out)

clean = make_game("limpio")
for pkg in packages:  # A primero, luego B encima (copiar y reemplazar)
    with zipfile.ZipFile(pkg) as z:
        z.extractall(clean)
game = clean / "game"
print("Tras copiar A y B:", sorted(p.name for p in (game / "tl").iterdir()), "| datos:", sorted(p.name for p in (game / "zz_linguanova/languages").iterdir()) if (game / "zz_linguanova/languages").is_dir() else "-")
script = (game / "zz_linguanova/linguanova.rpy").read_text(encoding="utf-8-sig")
print("linguanova.rpy viene de B; su lista escrita:", [l for l in script.splitlines() if l.startswith("# Languages when")])

# --- Ren'Py simulado ----------------------------------------------------------
block = script.split("init 999 python:\n", 1)[1]
body = []
for line in block.splitlines():
    if line and not line.startswith(" "):
        break
    body.append(line)
code = textwrap.dedent("\n".join(body))

class File:
    def __init__(self, p): self.h = open(p, "rb")
    def read(self): return self.h.read()
    def close(self): self.h.close()
files = [p.relative_to(game).as_posix() for p in game.rglob("*") if p.is_file()]
renpy = types.SimpleNamespace(
    list_files=lambda: files, file=lambda p: File(game / p),
    known_languages=lambda: ["russian", "spanish"],
    game=types.SimpleNamespace(preferences=types.SimpleNamespace(language="russian")),
    display=types.SimpleNamespace(screen=types.SimpleNamespace(screens={})),
    text=types.SimpleNamespace(text=types.SimpleNamespace(layout_cache_clear=lambda: None)))
config = types.SimpleNamespace(font_replacement_map={}, change_language_callbacks=[], always_shown_screens=[], overlay_screens=[], screen_height=720, screen_width=1280)
log = []
ns = {"renpy": renpy, "config": config, "persistent": types.SimpleNamespace(), "_preferences": renpy.game.preferences, "__name__": "store"}
exec(compile(code, "linguanova.rpy:init999", "exec"), ns)
print("Etiquetas leídas:", ns["_lntl_labels"])
print("Fuentes por idioma:", ns["_lntl_font_gaps"])
print("Menú de idiomas:", ns["_lntl_languages"]())
fmap = config.font_replacement_map
key = ("fonts/main.ttf", False, False)
print("Ruso activo -> main.ttf se reemplaza por:", fmap.get(key))
renpy.game.preferences.language = "spanish"; ns["_preferences"].language = "spanish"
print("Español activo -> main.ttf se reemplaza por:", fmap.get(key))
ok = "russian" in ns["_lntl_font_gaps"] and {"russian", "spanish"} <= set(c for c, _ in ns["_lntl_languages"]())
print("RESULTADO:", "los dos paquetes se suman" if ok else "FALLA")
