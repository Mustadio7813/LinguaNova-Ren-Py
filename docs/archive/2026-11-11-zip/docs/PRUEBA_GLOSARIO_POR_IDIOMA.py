"Revisión documental 2026-11-05_MODv5. Herramienta histórica conservada.\nLas opciones de idioma propias de esta variante se conservan. El selector y la detección no se confunden con el funcionamiento del MOD dentro del juego. El detector local se identifica como offline_py3langid; la propuesta de texto menos técnico sigue pendiente. La revisión v5 conserva los idiomas del juego y reúne los datos del MOD sin compartir variables entre archivos.\nConsultar GUIA_COMPLETA.md y las pruebas actuales. No se afirma haber ejecutado esta herramienta con sus requisitos externos en esta revisión.\n\nDescripción original:\nPrueba completa del glosario por idioma con un juego compilado por Ren'Py.\n\nUso: python probar_glosario_completo.py RUTA/LinguaNova_Traductor_RenPy.py JUEGO_COMPILADO\n- El personaje «Marcus» solo existe dentro de un .rpa (como .rpyc, sin fuente).\n- El glosario de español dice Shadow Sword -> Espada Sombría; el de francés,\n  Shadow Sword -> Épée de l'Ombre.\n- Se traduce con el pipeline real (CLI) al español y al francés, con un motor falso\n  que registra lo que recibe.\n"
import io, json, os, pickle, re, runpy, shutil, sys, tempfile, zlib
from pathlib import Path

target, source_game = sys.argv[1], Path(sys.argv[2])
os.environ["LINGUANOVA_DATA_DIR"] = tempfile.mkdtemp(prefix="ln_datos_")
work = Path(tempfile.mkdtemp(prefix="ln_juego_")) / "MiJuego"
shutil.copytree(source_game, work, ignore=shutil.ignore_patterns("cache", "saves"))
game = work / "game"
(work / "MiJuego.exe").write_text("exe")
(work / "MiJuego.py").write_text("# launcher")

# RPA-3.0 con personajes.rpyc y sin la fuente visible
def write_rpa(path, members):
    key = 0x42424242
    data = io.BytesIO(); data.write(b"RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n")
    index = {}
    for name, blob in members.items():
        offset = data.tell(); data.write(blob)
        index[name] = [(offset ^ key, len(blob) ^ key, b"")]
    index_offset = data.tell()
    data.write(zlib.compress(pickle.dumps(index, protocol=2)))
    raw = data.getvalue()
    header = b"RPA-3.0 %016x %08x\n" % (index_offset, key)
    path.write_bytes(header + raw[len(header):])
write_rpa(game / "archive.rpa", {"personajes.rpyc": (game / "personajes.rpyc").read_bytes()})
(game / "personajes.rpy").unlink(); (game / "personajes.rpyc").unlink()

if os.environ.get("LN_GLOSARIO_GLOBAL"):
    Path(os.environ["LINGUANOVA_DATA_DIR"], "glossary.json").write_text(json.dumps({"Shadow Sword": "Espada Sombría"}), encoding="utf-8")
g = runpy.run_path(target, run_name="ln_test")
PG = lambda n: g["LN_src_core_project_glossary__" + n]
if "LN_src_core_project_glossary__analyze" not in g:
    analysis=None

# 1) Análisis completo, solo en memoria
analysis = PG("analyze")(str(work))
print("Análisis: nombres", analysis.names, "| términos", analysis.terms[:6], "| scripts", analysis.script_files, "| compilados", analysis.compiled_files)
print("   ¿se escribió algo en disco por el análisis?", sorted(p.name for p in game.rglob("*glossary*")))

# 2) Glosarios por idioma
PG("save")(PG("glossary_path")(str(work), "spanish"), {"Shadow Sword": "Espada Sombría"}, "spanish")
PG("save")(PG("glossary_path")(str(work), "french"), {"Shadow Sword": "Épée de l'Ombre"}, "french")

# 3) Motor falso (Google) que registra lo que recibe
seen = []
WORDS = {
    "es": [("raised the", "levantó la"), ("over the valley.", "sobre el valle."), ("I met", "Conocí a"),
           ("near the old Mill yesterday.", "cerca del viejo molino ayer."), ("The ", "La "), ("glowed in the dark.", "brilló en la oscuridad.")],
    "fr": [("raised the", "a levé l'"), ("over the valley.", "au-dessus de la vallée."), ("I met", "J'ai rencontré"),
           ("near the old Mill yesterday.", "près du vieux moulin hier."), ("The ", "L'"), ("glowed in the dark.", "brillait dans le noir.")],
}
Result = g["LN_src_core_translators_base__TranslationResult"]
def fake(text, lang):
    out = text
    for a, b in WORDS[lang[:2]]:
        out = out.replace(a, b)
    return out
async def translate_single(self, request):
    seen.append((request.target_lang, request.text))
    protected, ph, _html = self._prepare_request_protection(request)
    final = g["LN_src_core_translators_google__restore_renpy_syntax"](fake(protected, request.target_lang), ph)
    return Result(request.text, final, request.source_lang, request.target_lang, request.engine, True)
async def translate_batch(self, requests):
    return [await translate_single(self, r) for r in requests]
Google = g["LN_src_core_translators_google__GoogleTranslator"]
Google.translate_single = translate_single
Google.translate_batch = translate_batch

# 4) Traducción real con la CLI, al español y al francés
main = g["LN_run_cli__main"]
for lang in ("es", "fr"):
    sys.argv = ["ln", "translate", str(work), "-t", lang, "-s", "en", "-e", "google", "--rpyc", "--no-extract-rpa", "--no-language-init"]
    try:
        code = main()
    except SystemExit as exc:
        code = exc.code
    print(f"CLI {lang}: código {code}")

def dialogue(folder):
    out = []
    for p in sorted((game / "tl" / folder).rglob("*.rpy")):
        for line in p.read_text(encoding="utf-8-sig").splitlines():
            s = line.strip()
            if s and not s.startswith("#") and ("Sword" in s or "Espada" in s or "Épée" in s or "Marcus" in s or "Eileen" in s):
                out.append(s)
    return out
es, fr = dialogue("spanish"), dialogue("french")
print("tl/spanish:", *es, sep="\n   ")
print("tl/french:", *fr, sep="\n   ")
sent_names = [t for _l, t in seen if "Marcus" in t or "Eileen" in t]
print("Solicitudes recibidas por el motor falso:", len(seen), seen[:4]); print("Textos enviados al motor que contenían Marcus/Eileen sin proteger:", sent_names)
checks = {
    "análisis encontró a Marcus dentro del .rpa": "Marcus" in analysis.names,
    "análisis encontró a Eileen": "Eileen" in analysis.names,
    "español usa Espada Sombría": any("Espada Sombría" in s for s in es),
    "español no contiene el término francés": not any("Épée" in s for s in es),
    "francés usa Épée de l'Ombre": any("Épée de l'Ombre" in s or "Épée de l\\'Ombre" in s for s in fr),
    "francés no contiene el término español": not any("Espada" in s for s in fr),
    "Marcus llega intacto a ambas traducciones": any("Marcus" in s for s in es) and any("Marcus" in s for s in fr),
    "el motor nunca recibió los nombres sin proteger": not sent_names,
    "cada idioma tiene su archivo de glosario (fuera de tl/)": (game / "zz_linguanova/glossary/spanish.json").is_file() and (game / "zz_linguanova/glossary/french.json").is_file() and not list((game / "tl").rglob("linguanova_glossary.json")),
}
for k, v in checks.items():
    print("OK   " if v else "FALLA", k)
print("RESULTADO:", sum(checks.values()), "/", len(checks))
