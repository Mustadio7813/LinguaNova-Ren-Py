<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


La preparación del entorno instala aparte las librerías opcionales de «Aligerar el juego» (`LN_start__ensure_optional`), después de las principales y antes de comprobar Qt:

- solo paquetes compilados (`--only-binary :all:`), un reintento y 20 s de espera;
- si fallan, LinguaNova abre igual y se reintenta como mucho una vez al día (estado en `linguanova-optional.json` dentro del entorno);
- la huella de `LN_DEPENDENCIES` no cambia, así que el entorno corto existente se reutiliza y no se vuelve a instalar PyQt6.

---

# ARRANQUE WINDOWS — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Windows usa un entorno corto externo, aislado por instalación, intérprete, arquitectura y dependencias. La comprobación carga un `Dialog Material` real. Los compiladores reciben la ruta preparada. Se mantienen los nombres cortos de las carpetas, aun cuando el ZIP japonés lleva una etiqueta legible. No se movieron entornos antiguos ni se tocaron los ajustes del usuario.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Arranque en Windows: ruta corta para Qt — 5 de noviembre de 2026

El registro recibido muestra que Windows no pudo cargar `qtquickcontrols2materialstyleimplplugin.dll` por la longitud de la ruta. El entorno de Python se creaba dentro de la carpeta descargada; el nombre largo del ZIP, la carpeta del programa, el entorno y las subcarpetas de Qt se acumulaban en la ruta de la DLL.

## Corrección

- En Windows, las dependencias se preparan fuera de la carpeta del programa, bajo una ruta corta de usuario: normalmente `%LOCALAPPDATA%\LN\v\p314-<identificador>`. Si esa ubicación resulta demasiado larga, se consideran ubicaciones cortas bajo el perfil de usuario o TEMP.
- El identificador separa instalaciones, intérpretes de Python, arquitecturas y conjuntos de dependencias. El nombre largo de la carpeta descargada no se añade a la ruta de las bibliotecas.
- El arranque normal usa este entorno incluso si el Python del sistema ya tiene las dependencias instaladas. Se mantiene la protección contra bucles de relanzamiento.
- La comprobación de dependencias ahora crea realmente un componente `Dialog` con el estilo `Material` de Qt, antes de abrir la aplicación. Un fallo conserva el mensaje completo y la ruta del intérprete en `inicio_error.log`.
- El proceso de Qt no hereda rutas de plugins de otras instalaciones de Qt.
- `COMPILAR.bat` y `COMPILAR_PORTABLE.bat` obtienen automáticamente la ruta del intérprete preparado. Se conserva el formato Windows de los BAT.
- Se acortaron los nombres de los ZIP y de sus carpetas interiores.

Los entornos anteriores no se trasladan ni se eliminan: la primera apertura prepara uno nuevo. La configuración de usuario, las claves y las traducciones siguen usando los mecanismos existentes. No se modifican los motores, el generador del MOD ni las correcciones previas de interfaz y de «Salir».

## Cómo abrir esta revisión

1. Cierra la ejecución anterior.
2. Extrae el ZIP en una carpeta nueva.
3. Ejecuta `INICIAR.bat` dentro de la carpeta del programa.
4. La primera vez se necesita Internet para preparar las dependencias en su nueva ubicación.

## Validación y alcance

Se probaron la selección de rutas Windows con espacios, acentos, caracteres Unicode, rutas largas y distintas versiones y arquitecturas de Python; la creación y reutilización real de un entorno; la carga real de `Dialog Material`; el registro de errores; la transferencia de la ruta de Python a los compiladores; y la conservación del resto del código.

La interfaz completa de ambas versiones se inició y cerró correctamente en Linux. No se dispone de Windows aquí, por lo que no se ejecutaron las DLL de Windows ni la compilación de un EXE en Windows. Las pruebas de selección de rutas simulan sus datos de plataforma.

Referencias técnicas:

- Microsoft: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
- Python: https://docs.python.org/3/library/venv.html
