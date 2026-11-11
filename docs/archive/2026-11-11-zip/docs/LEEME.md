<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Nueva herramienta en **Utilidades → Aligerar el juego** (modo avanzado): crea junto al juego una copia más liviana, con imágenes, audio y vídeo recomprimidos, sin tocar el original. Tiene **Calcular ahorro** (muestra, sin escribir nada) y **Crear copia optimizada**, tres niveles (Segura, Equilibrada y Máxima) y opciones para PC antiguo, motor solo de Windows y poca RAM. Conviene usarla después de traducir y generar el MOD: la copia los conserva.

El audio y el vídeo necesitan **ffmpeg**, un programa aparte. La versión portable lo descarga la primera vez que se usa la herramienta (o se elige un `ffmpeg.exe`); la versión en carpeta lo trae incluido. Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# Revisión actual de cobertura y Revisar

La traducción principal separa las copias exentas de los pendientes reales. Aplica una pasada acotada de recuperación y registra las líneas que siguen en la fuente en `translation_pending.json`. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md).

Al pulsar **Detener** en Revisar, el editor finaliza el trabajo, valida las respuestas disponibles y guarda las aceptadas con el respaldo y el control de conflictos existentes. Consulta [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

# Traductor de Ren'Py — Desarrollador

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

Abre `INICIAR.bat` tras extraer el ZIP en una carpeta nueva. La primera apertura prepara las dependencias. Para aplicar el arreglo a un juego ya traducido, cierra el juego y regenera su MOD.

Esta variante conserva el catálogo de idiomas de la edición original sin japonés. «Desarrollador» distingue el ZIP solicitado; las opciones previas de la aplicación conservan su comportamiento.

La [guía completa](GUIA_COMPLETA.md) contiene instalación, uso, motores, glosario, MOD, migración, cobertura, compilación, diagnóstico y límites.

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
