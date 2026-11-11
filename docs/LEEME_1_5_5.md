# LinguaNova Traductor de Ren'Py 1.5.5

Este paquete conserva las funciones de la edición adjunta y actualiza el nombre del producto. El ejecutable de Windows no se incluye: el entregable contiene código fuente auditable.

## Uso habitual
1. Extraer el paquete en una carpeta nueva.
2. Ejecutar `run.bat` en Windows, o `python LinguaNova_Traductor_RenPy.py`.
3. Añadir la carpeta o el ejecutable de un juego Ren’Py compatible.
4. Elegir el idioma y pulsar Traducir una sola vez.
5. Esperar la preparación: comprobación, traducción principal, textos de interfaz, instalación y verificación.
6. Pulsar Jugar cuando esté disponible. El programa vuelve a verificar los archivos al pulsarlo.

No se pregunta si el juego es sandbox, point and click o mixto. Esas categorías no determinan su compatibilidad técnica.

La primera ejecución puede instalar dependencias de terceros en `.venv_prueba_155`. No descarga ni reconstruye módulos propios de LinguaNova. Se necesita Python 3.10+; las pruebas de esta entrega se ejecutaron con Python 3.12/Linux. En Windows se incluye un BAT de compilación, pero no se ha ejecutado aquí.

## Aislamiento
La configuración, caché y los registros de la prueba usan una subcarpeta `LinguaNova/Prueba_1.5.5` del directorio de datos del usuario. Si se establece explícitamente LINGUANOVA_DATA_DIR, se respeta ese valor. No se migra ni sobrescribe la configuración de producción.

Los archivos del juego sí son un destino de la operación autorizada de traducción. Los respaldos se almacenan fuera de game/, en el directorio de datos de esta edición. Pruebe primero sobre una copia de su juego.

## MOD
En uso sencillo MOD muestra el panel opcional dentro del juego. La traducción no instala ese panel. Las herramientas independientes de traducción de interfaz y sus correcciones permanecen en modo avanzado. Traducir llama automáticamente al generador de interfaz, reutilizando las traducciones principales válidas; no instala dos copias de un hook multilenguaje.

## Cancelación y recuperación
Cancelar conserva el estado ocupado hasta que termina el worker. La traducción principal mantiene sus puntos de guardado existentes. La generación de interfaz puede cancelar y drenar solicitudes asíncronas y guarda las respuestas aceptadas. Una nueva ejecución comprueba el progreso y los archivos; no salta verificaciones porque una ejecución anterior figure como terminada.

Los cambios manuales detectados en archivos ya registrados se protegen a nivel de archivo completo. No es un sistema nuevo de aprobación por frase. Si un archivo protegido impide resolver un duplicado, se bloquea la preparación y se conserva el archivo.

## Recuperación avanzada
`python LinguaNova_Traductor_RenPy.py --restaurar "RUTA_DEL_JUEGO" --idioma spanish`

Restaura los respaldos verificados de la última operación y retira archivos nuevos registrados. Rechaza rutas fuera del juego, enlaces simbólicos y archivos modificados después de la operación. No restaura archivos ajenos ni elimina el panel opcional. Restaurar una preparación originalmente defectuosa puede restituir ese defecto; después de restaurar se deshabilita Jugar hasta otra preparación válida. Cierre el juego antes de recuperar.

## Resultado
- Preparado: resultados verificables disponibles; no garantiza calidad lingüística perfecta ni compatibilidad con todos los caminos de ejecución del juego.
- Parcial: se puede iniciar, pero hay textos pendientes, advertencias o correcciones protegidas.
- Detenido/error: no se habilita Jugar como resultado de esa operación.

Una imagen con texto no se traduce mediante OCR en esta versión.

## Aligerar una copia del juego

En **Utilidades → Aligerar el juego** (modo avanzado), calcula el ahorro o
crea una copia independiente con compresión de imágenes, audio y vídeo. El
original no se modifica. Hay opciones para compresión sin pérdida, equilibrada
o máxima, PCs antiguos, copias solo para Windows y equipos con poca RAM.
Consulta [la guía detallada](ALIGERAR_JUEGO.md).

La optimización de audio y vídeo necesita FFmpeg, un programa aparte. La
versión portable puede descargarlo al usar la herramienta; la versión en
carpeta puede incluirlo. Sin FFmpeg, audio y vídeo se copian sin cambios.
Prueba la copia optimizada antes de sustituir o borrar el original.

## DeepL y compilación

Selecciona DeepL en Traducir para ver el campo de clave y Guardar/Eliminar. Para compilar, ejecuta COMPILAR_1_5_5.bat; el ejecutable usa por defecto el perfil independiente Prueba_1.5.5_Compilado y no carga la clave guardada al ejecutar el .py. Ver ARREGLO_DEEPL_Y_COMPILACION_1_5_5.md.

## Nombre del producto

La aplicación y el ejecutable se llaman **LinguaNova Traductor de Ren'Py**. Consulta COMPILAR.md. Las carpetas internas de entorno y perfiles conservan sus identificadores anteriores para mantener el aislamiento y la compatibilidad de configuración. Los demás documentos de auditoría conservan el historial de la edición anterior.
