<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Todos los cambios son del 11 de noviembre de 2026. La versión de la aplicación sigue siendo 1.5.5.

| Área | Cambio |
| --- | --- |
| Utilidades | Tarjeta nueva **Aligerar el juego**: copia optimizada del juego y cálculo de ahorro, adaptados del Optimizador Ren'Py v3 sin consola. |
| Código | Módulos nuevos `src/tools/game_optimizer.py` y `src/backend/optimizer_backend.py` (`optimizerBackend`), componente `OptimizeGameCard.qml` y claves `opt_*` en los cinco idiomas. |
| ffmpeg | Se busca junto al programa, en `%LOCALAPPDATA%\LinguaNova\herramientas\ffmpeg`, en una ruta elegida y en el PATH. Descarga verificada por SHA-256 desde gyan.dev; opción `--descargar-ffmpeg`. |
| Dependencias | `LN_OPTIONAL_DEPENDENCIES` (pillow, pyoxipng, imagequant, mozjpeg-lossless-optimization), instaladas aparte y sin bloquear el arranque. El entorno principal no se reconstruye. |
| Compilación | `COMPILAR.bat` incluye ffmpeg en la carpeta del programa; `COMPILAR_PORTABLE.bat` no lo incluye. Ambos añaden `--hidden-import` de las librerías de imagen. |
| Cierre | Al cerrar la ventana se detiene una optimización en curso (ffmpeg y procesos incluidos). |
| No integrado | *Desempaquetar* del optimizador: LinguaNova ya extrae `.rpa` y lee `.rpyc` por su cuenta. |

Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# Revisión actual de cobertura y Revisar

La traducción principal separa las copias exentas de los pendientes reales. Aplica una pasada acotada de recuperación y registra las líneas que siguen en la fuente en `translation_pending.json`. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md).

Al pulsar **Detener** en Revisar, el editor finaliza el trabajo, valida las respuestas disponibles y guarda las aceptadas con el respaldo y el control de conflictos existentes. Consulta [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

<!-- 2026-11-05_MODv5 -->
# Historial completo de esta revisión

Todos los cambios descritos aquí pertenecen al 5 de noviembre de 2026. La versión de la aplicación sigue siendo 1.5.5; el formato del script del MOD pasa a v5.

| Área | Problema observado | Corrección y situación actual |
| --- | --- | --- |
| Cuadro final | Una franja recta sobresalía del borde redondeado | Se retiró la franja; permanece el contorno redondeado. |
| Resumen | Se mostraba la clave interna `trial_partial` o `trial_ready` | Se eliminó el prefijo; el resumen comienza con el texto del resultado. |
| Aviso temporal | Aparecía abajo y podía quedar detrás del cuadro modal | Se ubica arriba a la derecha, sobre la capa modal, y desaparece tras unos 3,5 segundos. |
| Texto de finalización | Aviso de finalización ausente o poco visible | Se conserva la distinción entre éxito, pendientes y error. En español, el éxito dice «La traducción terminó correctamente.». |
| Botones del juego | `Quit` se traducía como «Dejarlo» | `Quit`/`Exit` → «Salir» y `Quit Game`/`Exit Game` → «Salir del juego», solo para etiquetas completas de interfaz y destino español. Se conservan formato, mayúsculas y elecciones manuales o del glosario. |
| Bing | `ConfigManager` ocupaba el argumento del gestor de proxies | Su constructor pasa los argumentos por nombre. |
| Motores y MOD | Un error interno se convertía en numerosos intentos individuales | Se comprueban proxies al construir los motores y se propagan los errores internos reconocidos. Se cancelan las tareas pendientes y se conservan los reintentos transitorios de red. Se revisaron Google, Bing, DeepL, OpenAI, DeepSeek y Gemini. |
| Arranque Windows | Qt no cargaba Material por una ruta de DLL demasiado larga | Entorno externo corto, independiente de la longitud del directorio descargado. Se crea realmente un `Dialog Material` antes de abrir la aplicación. |
| Compiladores | Esperaban un Python dentro del proyecto | Ambos BAT leen la ruta del intérprete preparado. No se añade configuración personal al comando de compilación. |
| Título | Nombre y versión duplicados en la barra superior | El título y el nombre visible de Qt son exactamente «Traductor de Ren'Py». La versión sigue en los metadatos de la aplicación. |
| MOD dentro del juego | Dos scripts compartían `_lnmod_previous_replace_text`, generando recursión | Runtime v5 con funciones y estado en ámbito privado; registro común para unir idiomas; callback anterior estable; protección de reentrada y ante un callback antiguo recursivo. |
| Copias antiguas | Cambiar el nombre del proyecto dejaba varios `.rpy`/`.rpyc` activos | Salida estable `linguanova_mod_runtime_multilang.rpy`. Al regenerar se identifican scripts y bytecode propios obsoletos, se respaldan fuera de `game` y se retiran de forma transaccional. |
| Documentación | Guías, índices y resultados de fechas distintas se mezclaban | Todos los archivos de `docs` se actualizan o se identifican como históricos, con referencias al estado y las pruebas actuales. Se regeneran índices, diferencias y manifiestos. |

## Mensajes que no se han ocultado ni reinterpretado

`offline_py3langid` identifica el método local de detección del idioma; no es un error ni indica que la traducción se haga sin conexión. La propuesta de sustituirlo por «detectado automáticamente» sigue pendiente de confirmación y no se aplica en esta entrega.

«MOD incompleto» expresa cobertura parcial. En la captura del usuario: 61.958 traducidos + 358 pendientes + 159 que no necesitan cambio = 62.475 candidatos. Las 610 cadenas de código excluidas quedan fuera de ese total. El 99,2 % no certifica el funcionamiento completo del juego. No se conocen los motivos concretos de esos 358 pendientes porque no se recibió el informe JSON de esa ejecución.

## Antecedentes conservados

Los documentos anteriores sobre glosarios, navegación, cancelación, exportación, licencias e idiomas se conservan como antecedentes cuando aportan detalle. Sus mediciones antiguas no se presentan como pruebas de esta revisión. Los archivos originales y sus hashes conservan su significado de procedencia.
