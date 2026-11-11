'Revisión documental 2026-11-05_MODv5. Herramienta histórica conservada.\nLas opciones de idioma propias de esta variante se conservan. El selector y la detección no se confunden con el funcionamiento del MOD dentro del juego. El detector local se identifica como offline_py3langid; la propuesta de texto menos técnico sigue pendiente. La revisión v5 conserva los idiomas del juego y reúne los datos del MOD sin compartir variables entre archivos.\nConsultar GUIA_COMPLETA.md y las pruebas actuales. No se afirma haber ejecutado esta herramienta con sus requisitos externos en esta revisión.\n\nDescripción original:\nPrueba real del selector de idiomas de LinguaNova en Qt sin pantalla.\n\nUso: python probar_selector.py RUTA/LinguaNova_Traductor_RenPy.py\nAbre la aplicación real, hace clic con el ratón en las tarjetas de idioma y\ncomprueba que el panel se cierra, que el idioma cambia y que los dos paneles\nnunca quedan abiertos a la vez.\n'
import os, sys, runpy, json, tempfile

target = os.path.abspath(sys.argv[1])
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["LINGUANOVA_DATA_DIR"] = tempfile.mkdtemp(prefix="ln_datos_")
os.environ["QT_QUICK_BACKEND"] = "software"

from PyQt6 import QtQml, QtCore, QtGui
from PyQt6.QtTest import QTest

results = {"checks": [], "warnings": []}
Original = QtQml.QQmlApplicationEngine


def click(win, x, y):
    pt = QtCore.QPointF(x, y)
    for typ in (QtCore.QEvent.Type.MouseButtonPress, QtCore.QEvent.Type.MouseButtonRelease):
        btns = QtCore.Qt.MouseButton.LeftButton if typ == QtCore.QEvent.Type.MouseButtonPress else QtCore.Qt.MouseButton.NoButton
        ev = QtGui.QMouseEvent(typ, pt, win.mapToGlobal(pt), QtCore.Qt.MouseButton.LeftButton, btns, QtCore.Qt.KeyboardModifier.NoModifier)
        QtGui.QGuiApplication.sendEvent(win, ev)
        wait(30)


def wait(ms):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(ms, loop.quit)
    loop.exec()


class Engine(Original):
    def __init__(self, *a):
        super().__init__(*a)
        self.warnings.connect(lambda ws: results["warnings"].extend(w.toString() for w in ws))

    def load(self, url):
        super().load(url)
        QtCore.QTimer.singleShot(1500, self.run_tests)

    def ev(self, code):
        root = self.rootObjects()[0]
        expr = QtQml.QQmlExpression(QtQml.qmlContext(root), root, code)
        value, undefined = expr.evaluate()
        if expr.hasError():
            raise RuntimeError(expr.error().toString())
        return value.toVariant() if hasattr(value, "toVariant") else value

    def check(self, name, ok, detail=""):
        results["checks"].append({"prueba": name, "ok": bool(ok), "detalle": detail})

    def click_tile(self, side, index):
        root = self.rootObjects()[0]
        grid = "sourceMosaicGrid" if side == "source" else "targetMosaicGrid"
        pos = self.ev(f"(function(){{ var it = {grid}.itemAtIndex({index}); var p = it.mapToItem(null, it.width/2, it.height/2); return [p.x, p.y, {grid}.model[{index}].code] }})()")
        click(root, int(pos[0]), int(pos[1]))
        return pos[2]

    def click_item(self, item_id):
        root = self.rootObjects()[0]
        pos = self.ev(f"(function(){{ var p = {item_id}.mapToItem(null, {item_id}.width/2, {item_id}.height/2); return [p.x, p.y] }})()")
        click(root, int(pos[0]), int(pos[1]))

    def run_tests(self):
        try:
            root = self.rootObjects()[0]
            root.showNormal(); root.setGeometry(0, 0, 1400, 900); wait(800); results["ventana"] = [root.width(), root.height(), str(root.visibility())]
            self.ev("navIndex = 0"); wait(400)
            for side, other in (("source", "target"), ("target", "source")):
                combo, popup, other_popup = f"{side}LangCombo", f"{side}LangPopup", f"{other}LangPopup"
                getter = "getSourceLanguage" if side == "source" else "getTargetLanguage"
                for index in (1, 2, 0):
                    self.click_item(combo); wait(500)
                    self.check(f"{side}: se abre al pulsar el selector", self.ev(f"{popup}.opened"))
                    code = self.click_tile(side, index); wait(500)
                    opened = self.ev(f"{popup}.opened")
                    chosen = self.ev(f"appBackend.{getter}()")
                    shown = self.ev(f"{combo}.currentValue")
                    self.check(f"{side}: se cierra solo al elegir la tarjeta {index} ({code})", not opened, f"abierto={opened}")
                    self.check(f"{side}: idioma guardado = {code}", chosen == code or self.ev(f"appBackend.languageCode('{chosen}') === appBackend.languageCode('{code}')"), f"guardado={chosen}")
                    self.check(f"{side}: el selector muestra {code}", shown == chosen, f"mostrado={shown}")
                # Un panel abierto no puede convivir con el otro.
                self.click_item(combo); wait(500)
                self.click_item(f"{other}LangCombo"); wait(500)
                both = self.ev(f"{popup}.opened && {other_popup}.opened")
                self.check(f"{side}: nunca quedan los dos paneles abiertos", not both, f"origen={self.ev('sourceLangPopup.opened')} destino={self.ev('targetLangPopup.opened')}")
                self.ev(f"{popup}.close(); {other_popup}.close()"); wait(400)
                # Clic fuera del panel lo cierra.
                self.click_item(combo); wait(500)
                click(root, root.width() - 6, root.height() - 6); wait(500)
                self.check(f"{side}: un clic fuera del panel lo cierra", not self.ev(f"{popup}.opened"))
                # Esc lo cierra.
                self.click_item(combo); wait(500)
                QTest.keyClick(root, QtCore.Qt.Key.Key_Escape); wait(500)
                self.check(f"{side}: Esc lo cierra", not self.ev(f"{popup}.opened"))
                # Enter en el buscador elige el primero y cierra.
                self.click_item(combo); wait(500)
                [QTest.keyClick(root, ch) for ch in "fr"]; wait(200)
                QTest.keyClick(root, QtCore.Qt.Key.Key_Return); wait(500)
                self.check(f"{side}: Enter elige y cierra", not self.ev(f"{popup}.opened") and self.ev(f"appBackend.languageCode(appBackend.{getter}())") == "fr", f"guardado={self.ev(f'appBackend.{getter}()')}")
            if os.environ.get("LN_JUEGO_PRUEBA"):
                juego = os.environ["LN_JUEGO_PRUEBA"].replace("\\", "/")
                self.ev(f"appBackend.setProjectPath('{juego}')"); wait(1500)
                results["paquete_sugerido"] = self.ev("sharingBackend.suggestedPackageUrl()")
                if os.environ.get("LN_PROBAR_GLOSARIO"):
                    self.ev("appBackend.setTargetLanguage('spanish')"); wait(300)
                    self.ev("appBackend.addGlossaryItem('Shadow Sword', 'Espada Sombría')"); wait(300)
                    results["glosario_es"] = [str(x["source"]) + "=" + str(x["target"]) for x in self.ev("appBackend.glossaryList")]
                    results["glosario_es_texto"] = self.ev("appBackend.glossaryScopeText")
                    self.ev("appBackend.setTargetLanguage('french')"); wait(300)
                    results["glosario_fr_inicial"] = [str(x["source"]) + "=" + str(x["target"]) for x in self.ev("appBackend.glossaryList")]
                    self.ev("appBackend.addGlossaryItem('Shadow Sword', 'Épée de l Ombre')"); wait(300)
                    results["glosario_fr_texto"] = self.ev("appBackend.glossaryScopeText")
                    self.ev("appBackend.setTargetLanguage('spanish')"); wait(300)
                    results["glosario_es_otra_vez"] = [str(x["source"]) + "=" + str(x["target"]) for x in self.ev("appBackend.glossaryList")]
                    self.ev("appBackend.runToolGlossaryExtractor()"); wait(4000)
                    results["glosario_es_tras_extraer"] = [str(x["source"]) + "=" + str(x["target"]) for x in self.ev("appBackend.glossaryList")]
                    self.ev("navIndex = 4"); wait(500)
                btn = self.rootObjects()[0].findChild(QtCore.QObject, "createSharePackage")
                results["boton_encontrado"] = btn is not None
                if btn is not None:
                    QtCore.QMetaObject.invokeMethod(btn, "clicked"); wait(800)
                    dlg = [o for o in self.rootObjects()[0].findChildren(QtCore.QObject) if o.metaObject().className().startswith("QQuickFileDialog")]
                    results["dialogo"] = [(str(o.property("selectedFile")), str(o.property("currentFile")), o.property("visible"), o.metaObject().className()) for o in dlg]
            results["source_languages"] = [x["code"] for x in self.ev("appBackend.getSourceLanguages()")]
            results["target_languages"] = [x["code"] for x in self.ev("appBackend.getTargetLanguages()")]
        except Exception as exc:  # noqa: BLE001
            results["error"] = repr(exc)
        finally:
            print("RESULTADOS_JSON=" + json.dumps(results, ensure_ascii=False), flush=True)
            QtCore.QCoreApplication.exit(0)
            os._exit(0)


QtQml.QQmlApplicationEngine = Engine
sys.argv = [target, "--directo"]
runpy.run_path(target, run_name="__main__")
