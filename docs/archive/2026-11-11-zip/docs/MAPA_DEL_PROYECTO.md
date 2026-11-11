<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Piezas nuevas dentro de `LinguaNova_Traductor_RenPy.py`:

| Pieza | Ubicación |
| --- | --- |
| `src/tools/game_optimizer.py` | Prefijo `LN_src_tools_game_optimizer__`, justo antes del punto de entrada. |
| `src/backend/optimizer_backend.py` | `LN_src_backend_optimizer_backend__OptimizerBackend`, a continuación del anterior; se crea en `main` junto a `SharingBackend` y se publica como `optimizerBackend`. |
| `src/gui/qml/components/OptimizeGameCard.qml` | `LN_RESOURCE_src_gui_qml_components_OptimizeGameCard_qml`, después de `SharePackageCard.qml`; registrado en `qmldir` y `LN_RESOURCE_MAP`. |
| Uso en `Main.qml` | `viewToolbox > toolboxContent`, debajo de `SharePackageCard`. |
| Textos | Claves `opt_*` tras `share_package_skipped` en cada idioma de `LN_LOCALES`. |
| Dependencias opcionales | `LN_OPTIONAL_DEPENDENCIES`, `LN_OPTIONAL_IMPORTS` y `LN_start__ensure_optional` (después de `LN_start__prepare`). |
| Prueba | `docs/PRUEBA_ALIGERAR_JUEGO.py`. |

Las líneas exactas están en [INDICE_DEFINICIONES.json](INDICE_DEFINICIONES.json).

---

# Revisión actual de cobertura y Revisar

Las unidades de cobertura están en el parser de TL y el orquestador. El JSON nuevo se escribe junto a los diagnósticos. El backend de Revisar valida los resultados parciales con el editor antes de escribirlos. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md) y [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

# MAPA DEL PROYECTO — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

La aplicación sigue integrada en `LinguaNova_Traductor_RenPy.py`, con los BAT, recursos, licencias y documentación adjuntos. El código de los motores y del arranque conserva sus correcciones. Los cambios actuales se concentran en el título, el template del runtime v5, el autocontrol del hook y la publicación/migración de archivos propios.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Organización de la copia de prueba

- `LinguaNova_versión1.5.5_Prueba.py`: único código ejecutable de la aplicación. Contiene clases y funciones directas, QML legible, los cinco idiomas y recursos gráficos en memoria. No importa src/ ni extrae código propio.
- `INICIAR_PRUEBA.bat`: lanzador Windows de ese archivo.
- `COMPILAR_PRUEBA.bat`: prepara el entorno independiente y ejecuta PyInstaller sobre ese archivo plano.
- `docs/`: documentación de esta copia, auditoría, diferencias, pruebas y referencias históricas claramente marcadas.
- Archivos de licencia/procedencia: conservados de la entrega original.

El índice al principio del .py identifica cada componente QML con sus líneas INICIO/FIN. Todos los componentes, incluidas las opciones avanzadas, permanecen incrustados. El prefijo LN_ distingue símbolos que antes pertenecían a archivos diferentes; no representa módulos de ejecución nuevos.

## Implementaciones nuevas integradas
- trial_workflow: precomprobación, registro atómico, bloqueo por proyecto, inventario de fuentes, respaldos, protección de correcciones, cancelación, recuperación y verificación de preparación.
- trial_integrity: análisis de declaraciones old/new, reparación respaldada de duplicados y rescaneo de integridad.

Las rutas anteriores son nombres de procedencia empleados en comentarios para auditoría. No son dependencias de carpetas externas.

## Documentos del 5 de noviembre de 2026
- `docs/CORRECCION_SELECTOR_IDIOMAS.md`: paneles «Elegir idioma original / de destino»; prueba: `docs/PRUEBA_SELECTOR_IDIOMAS.py`.
- `docs/GLOSARIO.md`: glosario por juego e idioma y análisis temporal del juego; prueba: `docs/PRUEBA_GLOSARIO_POR_IDIOMA.py`.
- `docs/PAQUETE_COMPARTIR.md`: paquete ZIP/RAR, idiomas que se suman y archivos del SDK; pruebas: `docs/PRUEBA_PAQUETE_COMPARTIR.py`, `docs/PRUEBA_PAQUETES_SUMADOS.py`, `docs/PRUEBA_PAQUETE_SDK.py`.
- `docs/MOD_TRADUCCION_EXISTENTE.md`: el MOD sobre traducciones existentes (regla fija: no toca `game/tl/`); prueba con Ren'Py real: `docs/PRUEBA_MOD_TRADUCCION_EXISTENTE.py`.
- `docs/IDIOMAS.md`: idiomas de traducción, idiomas retirados y selector.
- Carpetas que LinguaNova usa dentro del juego: `game/tl/<idioma>/` (traducciones del traductor), `game/zz_linguanova/` (menú de idiomas, `languages/`, `glossary/`, `mod/`).
