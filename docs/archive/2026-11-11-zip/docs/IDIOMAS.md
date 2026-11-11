<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Se añadieron 60 claves `opt_*` (tarjeta, fases, mensajes e informe de «Aligerar el juego») en los cinco idiomas de la interfaz: español, inglés, francés, portugués y ruso. La prueba de interfaz cambia el idioma y comprueba el título y el botón principal de la tarjeta en cada uno. Los idiomas de traducción de juegos no cambian.

---

# IDIOMAS — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

La interfaz de la aplicación conserva sus cinco idiomas de interfaz. Los destinos de traducción dependen de la variante indicada en la guía completa de este paquete. Los idiomas existentes del juego se integran con el MOD; el runtime v5 une los datos de varias copias e idiomas y mantiene el idioma original sin traducir.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Idiomas de traducción

Los idiomas del traductor, la consola y el MOD se obtienen del catálogo común
`LN_src_utils_languages__LANGUAGES` dentro de `LinguaNova_Traductor_RenPy.py`.

| Idioma | Código | Carpeta del juego | DeepL | Google | Bing | IA |
| --- | --- | --- | --- | --- | --- | --- |
| Español | `es` | `tl/spanish` | `ES` | `es` | `es` | Spanish (Spain) |
| Inglés | `en` | `tl/english` | `EN-US` | `en` | `en` | English |
| Portugués (Brasil) | `pt-BR` | `tl/portuguese_brazil` | `PT-BR` | `pt-BR` | `pt` | Brazilian Portuguese |
| Francés | `fr` | `tl/french` | `FR` | `fr` | `fr` | French |
| Ruso | `ru` | `tl/russian` | `RU` | `ru` | `ru` | Russian |

Cada idioma conserva su carpeta, caché, memoria de traducción y datos del MOD.
Los idiomas de origen se envían al motor con su código base (`es`, `pt`, etc.).
El destino usa el código específico del motor indicado en la tabla.

Los nombres del selector siguen el idioma de la interfaz. Dentro del juego,
los nombres cortos proceden de `IN_GAME_NAMES` cuando existe una entrada.
La interfaz sigue disponible en español, inglés, francés, portugués y ruso.

La configuración antigua que guardaba `deepl_portuguese_variant=PT-BR` sigue
convirtiéndose a la carpeta `portuguese_brazil` del traductor y del MOD.

Para añadir un idioma al catálogo se indican su código, código base, carpeta
de Ren'Py, nombre para la IA, códigos de cada motor, nombres y alias.
Los selectores y las herramientas que consultan el catálogo se actualizan
desde esa misma entrada.

## Idiomas retirados

Español (Latinoamérica) y Portugués (Portugal) se retiraron. Si una configuración
guardada por una versión anterior los tenía elegidos (en el traductor o en el MOD),
el programa abre con Español o con Portugués (Brasil). Las carpetas
`tl/spanish_latam` y `tl/portuguese` que ya existan en un juego no se borran.

## Selector de idiomas

Los paneles «Elegir idioma original» y «Elegir idioma de destino» se cierran en
cuanto se elige un idioma (clic o Enter), con Esc o con un clic fuera del panel.
Al abrir uno se cierra el otro: nunca quedan los dos abiertos.
