"Revisión documental 2026-11-05_MODv5. Herramienta histórica conservada.\nEste documento se ha revisado en el contexto de la fuente actual: título «Traductor de Ren'Py», correcciones previas conservadas, runtime del MOD v5 y migración transaccional de scripts propios. Sus afirmaciones antiguas de pruebas, rutas o estructura se conservan como antecedentes identificados, no como evidencia de esta entrega. El estado completo y las limitaciones están en la guía y los resultados actuales.\nConsultar GUIA_COMPLETA.md y las pruebas actuales. No se afirma haber ejecutado esta herramienta con sus requisitos externos en esta revisión.\n\nDescripción original:\nEl MOD de LinguaNova sobre una traducción que NO hizo LinguaNova (Ren'Py real).\n\nUso: python probar_mod_ajeno.py RUTA/LinguaNova_Traductor_RenPy.py SDK JUEGO_ORIGEN CARPETA_TRABAJO [renombrar]\n\nJuego: «The Question» del SDK de Ren'Py, con su traducción oficial al español\n(game/tl/spanish), hecha por el equipo de Ren'Py. Se le añaden contenidos nuevos\nque esa traducción no cubre (2 líneas de diálogo y una pantalla de inventario).\nCon «renombrar», la traducción oficial se mueve a tl/espanol y se declara como\n«espanol», como hacen algunas traducciones de fans.\n"
import hashlib, json, os, runpy, shutil, subprocess, sys, tempfile
from pathlib import Path

target, sdk, origin, work = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
mode = sys.argv[5] if len(sys.argv) > 5 else ""
os.environ["LINGUANOVA_DATA_DIR"] = tempfile.mkdtemp(prefix="ln_datos_")
if work.exists():
    shutil.rmtree(work)
shutil.copytree(origin, work, ignore=shutil.ignore_patterns("cache", "saves", "*.rpyc", "traceback.txt", "log.txt", "errors.txt"))
game = work / "game"
(work / "TheQuestion.exe").write_text("exe")
with open(game / "script.rpy", "a", encoding="utf-8") as fh:
    fh.write('''
label ln_extra:
    "The merchant counted the coins slowly."
    "Sylvie smiled at the old lighthouse."
    return

default gold = 30

screen ln_inventory():
    vbox:
        text "Inventory"
        text "Gold: [gold]"
        textbutton "Sell all items" action NullAction()
''')
LANG = "spanish"          # carpeta de la traducción ajena
DECLARED = "spanish"      # idioma que declara en «translate <idioma>»
if mode == "renombrar":
    LANG = DECLARED = "espanol"
elif mode == "desconocido":
    LANG = DECLARED = "traduccion_fan"
elif mode == "duplicado":
    LANG = DECLARED = "espanol"
elif mode == "carpeta_distinta":
    LANG = "es_fan"
if LANG != "spanish":
    (game / "tl" / "spanish").rename(game / "tl" / LANG)
    if DECLARED != "spanish":
        for p in (game / "tl" / LANG).glob("*.rpy"):
            p.write_text(p.read_text(encoding="utf-8").replace("translate spanish ", "translate " + DECLARED + " "), encoding="utf-8")

official_backup = None
if mode == "futuro":
    official_backup = work.parent / (work.name + "_traduccion_oficial")
    if official_backup.exists():
        shutil.rmtree(official_backup)
    shutil.move(str(game / "tl" / "spanish"), str(official_backup))
    LANG = None
if mode == "conflictos":
    sp = game / "tl" / "spanish"
    t = (sp / "screens.rpy").read_text(encoding="utf-8")
    t = t.replace('    old "Load"\n    new "Cargar"', '    old "Load"\n    new "Load"', 1)   # copia sin traducir
    t = t.replace('    old "Save"\n    new "Guardar"', '    old "Save"\n    new ""', 1)      # vacía
    (sp / "screens.rpy").write_text(t, encoding="utf-8")
    t = (sp / "script.rpy").read_text(encoding="utf-8")
    t = t.replace('    "Nos casamos poco después de eso."', '    "We get married shortly after that."', 1)  # plantilla del SDK sin traducir
    (sp / "script.rpy").write_text(t, encoding="utf-8")
if mode == "duplicado":
    # Restos de un MOD anterior que creó un segundo idioma «spanish» con solo sus datos.
    (game / "tl" / "spanish").mkdir(parents=True, exist_ok=True)
    (game / "tl" / "spanish" / "linguanova_mod_hook_data.json").write_text('{"schema": 1, "mapping": {}, "contexts": {}}', encoding="utf-8")

PROBE = '''label splashscreen:
    python:
        import io, json
        def _say_what(node):
            what = getattr(node, "what", None)
            if what is None:
                for child in (getattr(node, "block", None) or []):
                    what = getattr(child, "what", None)
                    if what is not None:
                        break
            return what
        _tr = renpy.game.script.translator
        _out = {"languages": sorted(renpy.known_languages()), "preferencia": _preferences.language}
        _out["strings"] = {}
        for _lang in sorted(renpy.known_languages()):
            if _lang in ("spanish", "espanol", "traduccion_fan"):
                _out["strings"][_lang] = dict((s, renpy.translate_string(s, _lang)) for s in ["Start", "Load", "Save", "Inventory", "Sell all items", "Gold: [gold]"])
        _lines = ["We get married shortly after that.", "The merchant counted the coins slowly.", "Sylvie smiled at the old lighthouse."]
        _out["dialogue"] = {}
        for _lang in ("spanish", "espanol", "traduccion_fan"):
            if _lang not in renpy.known_languages():
                continue
            _d = {}
            for _ident, _node in _tr.default_translates.items():
                _what = _say_what(_node)
                if _what in _lines:
                    _t = _tr.language_translates.get((_ident, _lang))
                    _shown = _say_what(_t) if _t is not None else None
                    _shown = _shown if _shown else _what
                    _d[_what] = {"bloque_de_la_traduccion": _say_what(_t) if _t is not None else None, "se_ve": renpy.translate_string(_shown, _lang)}
            _out["dialogue"][_lang] = _d
        with io.open(config.basedir + "/sonda.json", "w", encoding="utf-8") as _f:
            _f.write(json.dumps(_out, ensure_ascii=False, indent=1))
        renpy.quit()
    return
'''

def run_game(tag, set_language=None):
    probe = game / "zz_linguanova_sonda.rpy"
    extra = ""
    if set_language:
        extra = '        renpy.change_language("%s")\n        renpy.save_persistent()\n' % set_language
    probe.write_text(PROBE.replace("        renpy.quit()\n", extra + "        renpy.quit()\n"), encoding="utf-8")
    (work / "sonda.json").unlink(missing_ok=True)
    env = dict(os.environ, SDL_AUDIODRIVER="dummy", RENPY_RENDERER="sw")
    subprocess.run(["xvfb-run", "-a", "-s", "-screen 0 1280x720x24", str(sdk / "renpy.sh"), str(work)], env=env, capture_output=True, timeout=300)
    probe.unlink()
    for name in ("zz_linguanova_sonda.rpyc",):
        (game / name).unlink(missing_ok=True)
    result = json.loads((work / "sonda.json").read_text(encoding="utf-8")) if (work / "sonda.json").is_file() else {"error": (work / "traceback.txt").read_text(encoding="utf-8")[-1500:] if (work / "traceback.txt").is_file() else "sin resultado"}
    run_game.last = result
    print(f"\n=== Juego en Ren'Py real: {tag}")
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return result

def digest(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob("*")) if p.is_file() and not p.name.endswith(".rpyc")}

foreign = game / "tl" / (LANG or "__ninguna__")
tl_before = sorted(p.name for p in (game / "tl").iterdir())
before_hash = digest(foreign) if foreign.is_dir() else {}
before_files = set(before_hash)
baseline = run_game("antes del MOD (solo la traducción oficial)")

# --- MOD de LinguaNova con un motor simulado ---------------------------------
g = runpy.run_path(target, run_name="ln_test")
Result = g["LN_src_core_translators_base__TranslationResult"]
restore = g["LN_src_core_translators_google__restore_renpy_syntax"]
PIECES = [("We get married shortly after that.", "Nos casamos poco después de aquello."), ("Load", "Cargar"), ("Save", "Guardar"), ("The merchant counted the coins slowly.", "El mercader contó las monedas despacio."),
          (" smiled at the old lighthouse.", " sonrió frente al viejo faro."),
          ("Sell all items", "Vender todos los objetos"), ("Inventory", "Inventario"), ("Gold: ", "Oro: ")]
sent = []
async def translate_single(self, request):
    sent.append(request.text)
    protected, ph, _html = self._prepare_request_protection(request)
    text = protected
    for a, b in PIECES:
        text = text.replace(a, b)
    return Result(request.text, restore(text, ph), request.source_lang, request.target_lang, request.engine, True)
async def translate_batch(self, requests):
    return [await translate_single(self, r) for r in requests]
Google = g["LN_src_core_translators_google__GoogleTranslator"]
Google.translate_single, Google.translate_batch = translate_single, translate_batch
config = g["LN_src_utils_config__ConfigManager"]()
manager = g["LN_src_backend_app_backend__TranslationManager"](g["LN_src_backend_app_backend__ProxyManager"](), config)
engine = g["LN_src_core_translators_base__TranslationEngine"].GOOGLE
manager.add_translator(engine, Google(proxy_manager=None, config_manager=config))
result = g["LN_src_ui_mod_generator__generate_interface_mod"](project_path=str(work), source_language="auto", target_language="spanish", engine=engine, translation_manager=manager)
print("\n=== Generación del MOD")
print("éxito:", result.success, "|", result.message)
g["LN_src_core_delivery__install"](str(game), config)  # lo que hace la app tras generar el MOD
if mode == "conflictos":
    # Corrección manual del usuario sobre un texto que la traducción oficial ya traduce
    lang_dir = g["LN_src_ui_mod_generator__mod_data_dir"](game, "spanish")
    (lang_dir / "linguanova_mod_manual.json").write_text(json.dumps({"schema": 1, "mapping": {"Start": "Empezar", "Inventory": "Mochila"}}), encoding="utf-8")
mod_folder = g["LN_src_ui_mod_generator__mod_data_dir"](game, g["LN_src_ui_mod_scanner__ModProjectScanner"]().language_id(str(work), "spanish")) if result.success else None
report = json.loads((mod_folder / "linguanova_mod_report.json").read_text(encoding="utf-8")) if mod_folder else {}
print("carpeta de datos del MOD:", mod_folder.relative_to(work) if mod_folder else None)
print("candidatos:", report.get("candidates"), "| origen de cada traducción:", report.get("origins"), "| pendientes:", report.get("pending"), "| sin cambio:", report.get("invariant"))
print("textos enviados al motor:", len(sent), sent[:8])
after_hash = digest(foreign) if foreign.is_dir() else {}
tl_after = sorted(p.name for p in (game / "tl").iterdir())
print("archivos de la traducción oficial modificados por LinguaNova:", sorted(k for k in before_hash if after_hash.get(k) != before_hash[k]))
print("archivos nuevos en", foreign.relative_to(work), ":", sorted(set(after_hash) - before_files))
print("carpetas de game/tl antes/después:", len(tl_before), "/", len(tl_after), sorted(set(tl_after) ^ set(tl_before)))
print("archivos nuevos en game/:", sorted(p.name for p in game.iterdir() if p.name.startswith(("linguanova_mod_", "zz_linguanova"))))
if mode == "futuro":
    run_game("con el MOD, sin traducción oficial (el jugador elige el idioma del MOD)", set_language="spanish")
    shutil.copytree(official_backup, game / "tl" / "espanol")
    for p in (game / "tl" / "espanol").glob("*.rpy"):
        p.write_text(p.read_text(encoding="utf-8").replace("translate spanish ", "translate espanol "), encoding="utf-8")
    for p in (game / "tl" / "espanol").glob("*.rpyc"):
        p.unlink()
    DECLARED = "espanol"
    run_game("el desarrollador añade su traducción «espanol» en una actualización (MOD sin regenerar)")
else:
    run_game("después del MOD de LinguaNova")

# --- Resumen respecto del objetivo: un único español, completo ---------------
final = run_game.last if hasattr(run_game, "last") else None
res = run_game.last
new_languages = sorted(set(res.get("languages", [])) - set(baseline.get("languages", [])))
if mode == "futuro":
    new_languages = [l for l in new_languages if l != "espanol"]
spanish_like = [l for l in res.get("languages", []) if l in ("spanish", "espanol", "traduccion_fan", "es_fan")]
strings = res.get("strings", {}).get(DECLARED, {})
dialogue = res.get("dialogue", {}).get(DECLARED, {})
checks = {
    "el MOD no añadió ningún idioma nuevo al juego (" + (", ".join(new_languages) or "ninguno") + ")": not new_languages and DECLARED in res.get("languages", []),
    "el MOD reutilizó la traducción ajena (" + str(report.get("origins", {}).get("existing_tl")) + " textos)": (report.get("origins", {}).get("existing_tl") or 0) > 100,
    "«Start» sigue con la traducción ajena": strings.get("Start") == "Comenzar",
    "«Inventory» lo completó el MOD": strings.get("Inventory") == "Inventario",
    "«Gold: [gold]» lo completó el MOD": strings.get("Gold: [gold]") == "Oro: [gold]",
    "diálogo de la traducción ajena intacto": dialogue.get("We get married shortly after that.", {}).get("se_ve") == "Nos casamos poco después de eso.",
    "diálogo nuevo completado por el MOD": dialogue.get("The merchant counted the coins slowly.", {}).get("se_ve") == "El mercader contó las monedas despacio.",
    "la traducción ajena intacta: ni cambios ni archivos nuevos": after_hash == before_hash,
    "el MOD no creó ni tocó carpetas en game/tl": set(tl_after) <= set(tl_before),
}
if mode == "conflictos":
    checks.pop("«Start» sigue con la traducción ajena", None)
    checks.pop("diálogo de la traducción ajena intacto", None)
    checks.pop("«Inventory» lo completó el MOD", None)
    checks["arrancó sin errores (sin «already exists»)"] = "error" not in res
    checks["«Load» copiado sin traducir -> lo rellena el MOD"] = strings.get("Load") == "Cargar"
    checks["«Save» vacío -> lo rellena el MOD"] = strings.get("Save") == "Guardar"
    checks["diálogo de la plantilla sin traducir -> lo rellena el MOD"] = dialogue.get("We get married shortly after that.", {}).get("se_ve") == "Nos casamos poco después de aquello."
    print("«Start» con corrección manual «Empezar» sobre la oficial «Comenzar» ->", strings.get("Start"))
    print("«Inventory» con corrección manual «Mochila» (la oficial no lo tiene) ->", strings.get("Inventory"))
if mode == "futuro":
    checks.pop("el MOD reutilizó la traducción ajena (" + str(report.get("origins", {}).get("existing_tl")) + " textos)", None)
    checks.pop("el paquete no lleva la traducción ajena", None)
    checks["un solo español tras la actualización (" + ", ".join(spanish_like) + ")"] = spanish_like == ["espanol"]
    checks["la preferencia del jugador pasó a «espanol» (" + str(res.get("preferencia")) + ")"] = res.get("preferencia") == "espanol"
if mode == "duplicado":
    checks["el idioma duplicado «spanish» ya no aparece en el juego"] = "spanish" not in res.get("languages", [])
    new_languages = []
# Paquete para compartir: de la traducción ajena solo deben viajar archivos de LinguaNova
import zipfile
pkg = work.parent / (work.name + "_paquete.zip")
try:
    built = g["LN_src_core_sharing__build_package"](str(work), str(pkg))
    names = zipfile.ZipFile(pkg).namelist()
    foreign_in_zip = [n for n in names if n.startswith("game/tl/" + (LANG or DECLARED) + "/") and not n.split("/")[-1].startswith("linguanova_")]
    print("\npaquete:", built.languages, "| archivos de la traducción ajena dentro:", foreign_in_zip[:5])
    checks["el paquete no lleva la traducción ajena"] = not foreign_in_zip
except Exception as exc:
    print("paquete:", exc)
print()
for k, v in checks.items():
    print("OK   " if v else "FALLA", k)
print("RESULTADO:", sum(checks.values()), "/", len(checks))
