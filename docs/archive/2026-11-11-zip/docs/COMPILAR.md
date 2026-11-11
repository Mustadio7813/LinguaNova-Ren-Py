<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


| BAT | ffmpeg | Librerías de imagen |
| --- | --- | --- |
| `COMPILAR.bat` (en carpeta, instalable) | Paso extra al final: copia `recursos\ffmpeg\ffmpeg.exe` si existe; si no, lo descarga verificado con `--descargar-ffmpeg` en `dist\<programa>\ffmpeg\`. Si falla, avisa y el EXE lo ofrecerá al usarlo. | `--hidden-import` de Pillow, oxipng, imagequant y mozjpeg. |
| `COMPILAR_PORTABLE.bat` (un solo EXE) | No se incluye, para que el EXE siga siendo liviano y abra rápido; la herramienta lo descarga la primera vez o el usuario elige un `ffmpeg.exe`. | Igual. |

Para compilar la versión en carpeta sin Internet, deja `ffmpeg.exe` (y si quieres `LICENSE_ffmpeg.txt`) en `recursos\ffmpeg\`. Al repartir esa versión, la carpeta `ffmpeg` va con su licencia GPL; el código fuente está en https://ffmpeg.org/download.html. Las librerías de imagen se incluyen si estaban instaladas en el entorno de compilación (las instala la preparación de forma opcional). Los EXE no se compilaron en Windows en esta revisión. Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# COMPILAR — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Los dos BAT de compilación leen la ruta que devuelve la preparación del entorno; ya no presuponen un `.venv_prueba_155` local en Windows. El modo carpeta necesita su `_internal`; el modo portable produce un único ejecutable. Se conserva la preparación sin configuración personal y la imagen de carga opcional cuando hay Tcl/Tk. Los ejecutables no se compilaron en Windows durante esta revisión.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Compilar en Windows

1. Colocar COMPILAR.bat junto a LinguaNova_Traductor_RenPy.py.
2. Ejecutar el BAT. Requiere Python 3.10+ e Internet para preparar las dependencias si faltan.
3. Esperar a que termine; el progreso técnico queda en compilacion_error.log.
4. El ejecutable queda en dist/LinguaNova Traductor de Ren'Py/LinguaNova Traductor de Ren'Py.exe.
5. Distribuir la carpeta dist/LinguaNova Traductor de Ren'Py completa, incluido _internal. No distribuir la carpeta de desarrollo, AppData, config.json ni archivos .env.

## Versión portable (un solo .exe)

1. Ejecutar **COMPILAR_PORTABLE.bat**, junto a LinguaNova_Traductor_RenPy.py. Usa el mismo entorno externo de ruta corta que prepara COMPILAR.bat.
2. La ventana indica el paso en curso (1 de 3: preparar Python y dependencias; 2 de 3: PyInstaller; 3 de 3: compilar). Durante cada paso no muestra más texto: el detalle se va escribiendo en compilacion_portable_error.log. La primera vez el paso 1 puede tardar de 5 a 15 minutos.
3. El resultado es un solo archivo: dist_portable/LinguaNova Traductor de Ren'Py.exe, con Qt, Python y el programa dentro. Se reparte tal cual, sin carpeta `_internal`.
4. Al abrirse se descomprime en una carpeta temporal de Windows, por eso tarda unos segundos más que la versión en carpeta. Algunos antivirus revisan este tipo de ejecutables con más calma.

Por qué COMPILAR.bat genera un .exe de pocos MB: en modo carpeta el .exe solo arranca el programa; Qt y Python (más de 100 MB) van en `_internal`, a su lado. Copiar únicamente el .exe no funciona.

Comprobación en Linux con el mismo código: la versión portable pesó 138 MB en un solo archivo, compiló en un minuto y abrió la interfaz completa. En Windows el tamaño será parecido. El actualizador automático integrado espera la versión en carpeta (`LinguaNova.exe` y su `_internal`); el portable se actualiza descargando el .exe nuevo.

## Ícono y pantalla de carga

- Los dos BAT usan `recursos/linguanova.ico` como ícono del `.exe` (el que se ve en el Explorador, el escritorio y la barra de tareas). Si falta ese archivo, la compilación se detiene con un aviso en el registro.
- El programa usa el mismo ícono en su ventana y muestra el logo en grande mientras carga («Loading LinguaNova…»).
- Con `--splash`, el `.exe` muestra `recursos/linguanova_splash.png` desde el primer instante, mientras se descomprime; el programa la cierra al aparecer su propia pantalla de carga. Esto necesita Tcl/Tk, que incluye el Python de python.org. Si falta, el BAT compila igual y lo indica en la ventana.
- Si Windows sigue mostrando el ícono antiguo en un `.exe` recién compilado, es la caché de íconos del Explorador: cambia el nombre del archivo o cierra sesión y vuelve a entrar.

## Notas

El BAT no requiere el lanzador INICIAR.bat. La clave de DeepL guardada al probar el .py no se incorpora al ejecutable. El .exe usa un perfil local separado y cada usuario introduce su propia clave.

No es necesario insertar una clave en el código fuente para compilar. El compilador no comprueba si una clave es válida ni contacta con DeepL. Esta receta no se ejecutó en Windows durante la validación realizada aquí.

El nombre del ejecutable y de la aplicación es **LinguaNova Traductor de Ren'Py**. Los espacios y el apóstrofo se pasan entre comillas al compilador. La versión continúa siendo 1.5.5.
