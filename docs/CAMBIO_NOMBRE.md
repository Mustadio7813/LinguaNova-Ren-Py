# CAMBIO NOMBRE — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El proyecto y sus avisos siguen identificados como LinguaNova. El título visible de la ventana es exactamente «Traductor de Ren'Py». Los archivos distribuidos se distinguen por «Desarrollador» y «Japones_日本語». La carpeta interior mantiene un nombre corto para no repetir el problema de la ruta de Qt.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Cambio de nombre — 2026-11-03

Nombre del producto: **LinguaNova Traductor de Ren'Py**. Versión: **1.5.5**.

Se actualizan el nombre de salida de PyInstaller, las rutas de comprobación y los mensajes del compilador; el nombre Qt de la aplicación y su nombre visible; y el título principal QML, que conserva el nombre del producto al cambiar de idioma. Las etiquetas cortas de la marca dentro de la interfaz se mantienen para preservar su distribución.

Archivos de uso actual:
- `LinguaNova_Traductor_RenPy.py`
- `INICIAR.bat`
- `COMPILAR.bat`
- `docs/LEEME.md`
- `docs/COMPILAR.md`

No se implementan funciones nuevas de traducción. Se conservan las dependencias, licencias, avisos de procedencia, perfiles separados del código fuente y del ejecutable y exclusión de configuración personal de la compilación. Los identificadores internos e informes de auditoría anteriores se conservan por compatibilidad e historial; los hashes de esos informes describen la entrega previa.

Validación de esta modificación: sintaxis Python; comparación estructural del código con el adjunto; comprobación de coherencia de nombres y rutas del BAT y del título QML integrado. El BAT se guarda con finales de línea CRLF. No se ha ejecutado la compilación Windows en este entorno Linux.
