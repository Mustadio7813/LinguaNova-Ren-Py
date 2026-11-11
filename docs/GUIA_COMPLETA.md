<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


## Aligerar el juego

1. Activa el modo avanzado en **Ajustes** y abre **Utilidades**.
2. Con el juego abierto, en la tarjeta **Aligerar el juego** elige la compresión (Equilibrada es la recomendada) y las opciones:
   - **Modo PC antiguo**: solo para una copia destinada a un PC donde los vídeos van a tirones (720p, 30 fps, formato más ligero).
   - **Quitar los archivos del motor para Linux y Mac**: si la copia solo se usará en Windows.
   - **Ajustes para PC con poca memoria RAM**: añade `game/zz_gama_baja.rpy`.
3. **Calcular ahorro** estima el resultado con una muestra; no escribe nada.
4. **Crear copia optimizada** pide la carpeta y crea `<juego>_Optimizado`, más el informe `<juego>_Optimizado_informe.txt`.
5. Prueba la copia antes de borrar o reemplazar el original. **Detener** no deja copias a medias.

Si la tarjeta avisa de que falta ffmpeg, pulsa **Descargar ffmpeg (~100 MB)** (Windows) o **Elegir ffmpeg.exe…**. Sin ffmpeg solo se comprimen las imágenes. Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# Revisión actual de cobertura y Revisar

La traducción principal separa las copias exentas de los pendientes reales. Aplica una pasada acotada de recuperación y registra las líneas que siguen en la fuente en `translation_pending.json`. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md).

Al pulsar **Detener** en Revisar, el editor finaliza el trabajo, valida las respuestas disponibles y guarda las aceptadas con el respaldo y el control de conflictos existentes. Consulta [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

<!-- 2026-11-05_MODv5 -->
# Guía completa — Traductor de Ren'Py 1.5.5

## Paquetes y título

Esta carpeta pertenece a **Desarrollador**. Archivo distribuido: **LinguaNova_Desarrollador.zip**. La barra de la ventana muestra exactamente **Traductor de Ren'Py**. El nombre interno del proyecto y los avisos de licencia de LinguaNova se conservan.

Esta variante conserva el catálogo de idiomas de la edición original sin japonés. «Desarrollador» distingue el ZIP solicitado; las opciones previas de la aplicación conservan su comportamiento.

## Abrir la aplicación

1. Cierra la ejecución anterior y extrae el ZIP en una carpeta nueva.
2. Ejecuta `INICIAR.bat`. Se requiere Python 3.10 o posterior.
3. En la primera apertura se necesita Internet para instalar dependencias.

En Windows el entorno se crea normalmente en `%LOCALAPPDATA%\LN\v\<identificador>`, separado por instalación, intérprete, arquitectura y dependencias. Si esa ruta es excesiva, se consideran ubicaciones cortas del perfil de usuario o TEMP. No se traslada ni se borra el entorno antiguo. El lanzador verifica importaciones y crea un componente real `Dialog Material`; el detalle de un fallo queda en `inicio_error.log`. Las rutas de plugins de otra instalación de Qt no se heredan al abrir el proceso.

La configuración existente continúa en el perfil de usuario usado por la aplicación. Mover el entorno de dependencias no convierte los ajustes ni las claves en código fuente. No copies la configuración personal al compartir el programa.

## Traducción y MOD

La página Traducción procesa la traducción del juego y puede preparar su interfaz mediante el mismo generador. La página MOD permite generar ese complemento de forma separada. El MOD se integra con los idiomas del propio juego; no añade un selector de idiomas propio dentro del juego.

Selecciona el proyecto, el idioma de destino y el motor disponibles en la interfaz. La detección automática usa evidencia del texto; la etiqueta de origen informa de la ruta utilizada. `en` significa inglés y `es`, español. `offline_py3langid` es un detector local, independiente del motor que traduce. Ese texto técnico no se ha cambiado sin la confirmación solicitada por el usuario.

Los motores disponibles son Google, Bing, DeepL, OpenAI, DeepSeek y Gemini. Las claves y las condiciones de cada servicio son independientes de los errores de programación. El fallo concreto de Bing era un intercambio de argumentos, no una cuota. La protección común detiene los errores internos reconocidos; los errores transitorios conservan sus reintentos. Las pruebas con respuestas simuladas no validan credenciales reales ni garantizan la disponibilidad externa de cada proveedor.

## Archivos del MOD

- `game/linguanova_mod_runtime_multilang.rpy`: script estable que registra las traducciones y los callbacks.
- `game/zz_linguanova/mod/<idioma>/linguanova_mod_hook_data.json`: datos y procedencia.
- `game/zz_linguanova/mod/<idioma>/linguanova_mod_manual.json`: correcciones manuales.
- `game/zz_linguanova/mod/<idioma>/linguanova_mod_report.json`: cobertura, pendientes, motivos, fuentes, archivos retirados y respaldo.

Los datos de otros idiomas se incorporan al mismo script. El juego conserva su traducción nativa; el MOD completa lo que corresponde. Puede asociarse a un idioma ya existente con otro nombre equivalente. El generador no crea nuevas traducciones nativas bajo `game/tl/`; las migraciones de restos antiguos reconocidos se identifican y respaldan.

## Actualizar un MOD ya generado

Actualizar el traductor no cambia automáticamente los archivos de un juego. Cierra el juego y vuelve a generar el MOD con esta revisión. Se reutilizan datos válidos y correcciones manuales, por lo que no se exige volver a enviar todos los textos al motor.

Las copias propias obsoletas de `linguanova_mod_*_multilang.rpy` y sus `.rpyc` se identifican por su cabecera o por marcadores del bytecode descomprimido, sin deserializarlo. Se respaldan bajo `.linguanova_backups/mod_hooks/` al lado de `game`. Se elimina también la caché compilada propia que deba reconstruirse. Los scripts ajenos no se retiran. La publicación restaura las versiones anteriores si falla un reemplazo o una retirada.

El runtime v5 usa un ámbito privado para evitar que dos archivos sobrescriban el callback anterior o las cachés del otro. Un registro en el módulo de Ren'Py reúne los idiomas y sustituye sus propios callbacks anteriores. Conserva callbacks del juego, protege la reentrada y puede desconectar un predecesor antiguo que recursiona. Se inicia después de los hooks v4 de prioridad 990.

## Interpretar el resultado

«Traducido» cuenta textos con una traducción aceptada. «Sin cambio» cuenta textos invariantes; no significa que el motor haya fallado. «Pendiente» significa que el texto no obtuvo una traducción válida y puede seguir en el idioma original. El código y los textos técnicos excluidos no forman parte del total de candidatos traducibles.

Ejemplo de la captura recibida: 61.958 traducidos, 358 pendientes y 159 sin cambio suman 62.475 candidatos; el porcentaje mostrado es 99,2 %. Se excluyeron además 610 cadenas de código. Para diagnosticar cada pendiente, lee `pending_reasons`, `pending_texts` y `pending_by_file` del informe generado. Esta revisión no afirma conocer los motivos de aquel informe que no se adjuntó.

## Glosario, fuentes y correcciones

El glosario conserva el alcance por juego y por idioma. Las correcciones manuales y los términos explícitos tienen prioridad en sus rutas existentes. El reemplazo de «Quit/Exit» solo se aplica a etiquetas completas de interfaz; no sustituye globalmente «dejarlo» en los diálogos.

Los planes de fuentes y el idioma activo se mantienen por idioma. Las sustituciones propias se retiran al cambiar al idioma original o a otro idioma. El MOD respeta las traducciones nativas existentes y evita registrar dos veces una misma traducción.

## Compilar y distribuir

Usa `COMPILAR.bat` para una carpeta de distribución completa o `COMPILAR_PORTABLE.bat` para un ejecutable único. Ambos preparan las dependencias y reciben la ruta del intérprete actual. El ejecutable pequeño de la modalidad carpeta necesita su directorio `_internal`; su tamaño aislado no representa el paquete completo. La imagen de carga se usa si Tcl/Tk está disponible.

Comparte la distribución generada o el paquete de traducción correspondiente; no incluyas claves, configuraciones personales, cachés de desarrollo ni entornos de Python. Conserva `LICENSE`, `COPYING` y los avisos de terceros. El nombre «Desarrollador» del ZIP identifica la variante solicitada y no cambia por sí mismo el régimen de licencia ni desbloquea funciones.

## Diagnóstico y pruebas

- Inicio y Qt: `inicio_error.log`, además del registro de la aplicación.
- Compilación: `compilacion_error.log` o `compilacion_portable_error.log`.
- MOD: informe JSON del idioma y registro `log.txt` del juego para fallos de ejecución.
- Pruebas actuales: [RESULTADOS_PRUEBAS.md](RESULTADOS_PRUEBAS.md), [PRUEBAS_RENPY_744.json](PRUEBAS_RENPY_744.json) y los scripts de comprobación descritos en el índice.

Se reprodujo la recursión de los dos hooks v4 y se ejecutaron los hooks corregidos en el SDK oficial **Ren'Py 7.4.4.1439 para Linux**, la misma versión de motor que aparece en la traza. También se comprueban copias v5 múltiples, mezcla v4/v5, idiomas, traducciones nativas, retirada de fuentes/bytecode propios y restauración transaccional. Se ejecutó una prueba de 62.476 entradas con dos copias del hook, y una prueba de guardado y carga reales del SDK usando una captura PNG de prueba para no requerir OpenGL en el entorno sin pantalla.

No se ejecutó el juego completo Another Chance ni las DLL o la compilación nativas de Windows. Los cambios de rutas Windows se verifican con datos de plataforma simulados; la interfaz Qt se inicia en Linux. Los resultados antiguos de `docs` se identifican como históricos y no sustituyen estas pruebas.

## Documentación, procedencia e índice

[HISTORIAL_CAMBIOS.md](HISTORIAL_CAMBIOS.md) reúne los cambios de esta conversación. [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md) describe todos los archivos. `INDICE_DEFINICIONES.json` refleja las líneas de esta fuente; `MANIFIESTO_PRUEBA.json` contiene tamaños y hashes actuales, con exclusión explícita de sí mismo. Los datos originales se conservan como procedencia histórica.

Referencias: [Python de Ren'Py](https://www.renpy.org/doc/html/python.html), [rutas de Windows](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation), [entornos de Python](https://docs.python.org/3/library/venv.html).
