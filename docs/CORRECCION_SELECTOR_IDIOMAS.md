# CORRECCION SELECTOR IDIOMAS — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Las opciones de idioma propias de esta variante se conservan. El selector y la detección no se confunden con el funcionamiento del MOD dentro del juego. El detector local se identifica como offline_py3langid; la propuesta de texto menos técnico sigue pendiente. La revisión v5 conserva los idiomas del juego y reúne los datos del MOD sin compartir variables entre archivos.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Corrección de los paneles de idioma (5 de noviembre de 2026)

## Problemas

1. Los paneles «Elegir idioma original» y «Elegir idioma de destino» podían
   quedar abiertos a la vez, uno encima del otro.
2. Un clic fuera del panel no lo cerraba: había que pulsar la «×».
3. Al elegir un idioma, el panel podía seguir abierto.

## Causas

- Los paneles se dibujan sobre toda la ventana (`parent: Overlay.overlay`), pero
  conservaban la regla de cierre del menú desplegable original,
  `CloseOnPressOutsideParent`. Como su «padre» era la ventana entera, ningún clic
  quedaba fuera y nunca se cerraban solos. Por la misma razón, abrir el segundo
  panel no cerraba el primero.
- Al pulsar una tarjeta se aplicaba el idioma antes de cerrar. Aplicarlo refresca
  la interfaz (`refreshUI`), rehace la lista de tarjetas y elimina la tarjeta que
  recibió el clic; según la versión de Qt, la orden de cierre que venía después ya
  no se ejecutaba.

## Cambios (solo QML, dentro de `LinguaNova_Traductor_RenPy.py`)

- Cada panel tiene `chooseLanguage(code)`: cierra el panel y aplica el idioma
  justo después (`Qt.callLater`). La tarjeta y la tecla Enter usan esta función.
- Los paneles son modales sin oscurecer la ventana (`modal: true`, `dim: false`)
  y se cierran con `CloseOnEscape | CloseOnPressOutside`. Un clic fuera solo
  cierra el panel; no abre otro sin querer.
- Al abrir un panel se cierra el otro si estaba abierto.

El aspecto, los textos y los tamaños no cambian.

## Comprobación

Se ejecutó la interfaz real (PyQt6 6.10, Qt sin pantalla) con clics de ratón y
teclas simulados sobre las tarjetas reales, en los dos paneles:

- abrir el panel, elegir tres idiomas distintos y comprobar que se cierra, que el
  idioma queda guardado y que el selector lo muestra;
- abrir un panel y pulsar el otro selector: nunca quedan los dos abiertos;
- clic fuera del panel, Esc, y escribir en el buscador + Enter.

Resultado: 32 de 32 comprobaciones correctas. La versión anterior fallaba 4:
los dos paneles quedaban abiertos a la vez y el clic fuera no los cerraba.
También se comprobó que el programa compila y que los índices de la cabecera y
`docs/INDICE_DEFINICIONES.json` apuntan a las líneas correctas.

No se probó en Windows ni con un juego real; el cambio no toca la traducción.

## Idiomas retirados en esta versión

Se quitaron Español (Latinoamérica) y Portugués (Portugal) con los mismos
cambios que ya tenía la versión con japonés (catálogo, avisos de variante,
códigos de DeepL, MOD y consola), sin añadir japonés. También se incluyó la
corrección del cierre `AppBackend._t() missing 1 required positional argument`,
que podía cerrar el programa con cualquier idioma.

Una configuración guardada con alguno de esos dos idiomas abre ahora con Español
o Portugués (Brasil). Comprobado cargando configuraciones guardadas con
`spanish_latam` y `portuguese` en el traductor y en el MOD.

Idiomas de destino: Español, Inglés, Portugués (Brasil), Francés y Ruso.
