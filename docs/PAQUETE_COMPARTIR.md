<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


«Compartir o respaldar traducciones» y «Aligerar el juego» son independientes. El paquete lleva solo las traducciones y los datos de LinguaNova; la copia optimizada es el juego completo, más liviano, con esas mismas traducciones dentro. La copia no incluye `.linguanova_backups/`: los respaldos se quedan con el juego original.

---

# PAQUETE COMPARTIR — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El paquete reúne las traducciones y los datos propios de LinguaNova para el mismo juego. Conserva el menú de idiomas del juego y los idiomas que se suman de varios paquetes. La revisión actual del runtime es v5 y su archivo estable es `linguanova_mod_runtime_multilang.rpy`. Las claves, los ajustes privados y los entornos de Python no deben distribuirse.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Paquete para compartir traducciones (5 de noviembre de 2026)

## Qué incluye

El botón «Crear ZIP / RAR» guarda **solo los idiomas hechos con LinguaNova**, con
las mismas rutas que tienen dentro del juego:

- cada carpeta `game/tl/<idioma>` hecha con LinguaNova, completa: las traducciones,
  los archivos que Ren'Py genera para ese idioma (`common.rpy`, `.rpyc`, etc.),
  los manifiestos de la salida (`.linguanova/`) y los datos del MOD;
- los scripts que LinguaNova añade a `game/` (menú de idioma, runtime, MOD) y sus
  carpetas de fuentes (`zz_linguanova`, `linguanova_fonts`, `linguanova_mod_fonts`).

No incluye partidas guardadas (`saves`), la caché de Ren'Py, diagnósticos ni los
idiomas que el juego ya traía. Los idiomas que se quedan fuera aparecen en el
registro al terminar.

## Cómo se reconoce un idioma de LinguaNova

Una carpeta `game/tl/<idioma>` cuenta si tiene al menos una de estas marcas:

1. un `.rpy` cuya cabecera empieza por `# LinguaNova bounded translation output v1`
   (o las marcas de versiones anteriores);
2. un manifiesto `.linguanova/linguanova_output_*.json`;
3. datos del MOD `linguanova_mod_*.json`;
4. el informe de cobertura `tl/.diagnostics/<idioma>/coverage_by_category.json`,
   que LinguaNova deja al traducir. Así se reconocen también los idiomas cuyos
   archivos generó el SDK de Ren'Py y LinguaNova tradujo en su sitio (esos
   archivos no llevan la marca de cabecera).

`tl/None` nunca se incluye.

## Instalación (la que explica el LÉEME del paquete)

Descomprimir, copiar la carpeta `game/` sobre la del juego (misma versión) y
aceptar reemplazar. Después se elige el idioma en las Preferencias del juego.

## Nombre propuesto

Al pulsar el botón, el diálogo propone `<juego>_LinguaNova_<idiomas>.zip` en la
carpeta del juego (fuera de `game/`). Se puede cambiar el nombre o la carpeta.

## Comprobación

Con un juego de prueba que tenía `tl/None`, un francés oficial del juego, un
español hecho con LinguaNova (con archivos de Ren'Py, `.rpyc`, subcarpeta,
manifiesto y diagnósticos), un ruso con la marca antigua y un japonés solo del MOD:

- el paquete contuvo español, ruso y japonés, y dejó fuera el francés y `tl/None`;
- no incluyó `saves`, `cache` ni `diagnostics`;
- al descomprimirlo sobre una copia limpia del juego, cada archivo quedó en su ruta
  original con el mismo contenido (comparación byte a byte);
- un juego sin idiomas de LinguaNova muestra «game/tl no contiene traducciones
  hechas con LinguaNova.»;
- en la interfaz real, el botón abre el diálogo con el nombre propuesto
  (`Mi_Juego_1.0_LinguaNova_japanese_russian_spanish.zip`) sin errores de QML.

## Varios paquetes sobre el mismo juego

Cada idioma instalado deja `game/zz_linguanova/languages/<idioma>.json` con su nombre
y las fuentes del juego que no pueden dibujarlo (por ejemplo, una fuente sin
cirílico para el ruso). `zz_linguanova/linguanova.rpy` lee todos esos archivos al
abrir el juego. Por eso, si se copian varios paquetes uno encima de otro, los
idiomas se suman: el último `linguanova.rpy` copiado ya no borra la corrección de
fuentes de los idiomas que trajeron los paquetes anteriores. La lista de idiomas
del menú ya salía de Ren'Py al abrir el juego (`renpy.known_languages()`).

Cada vez que LinguaNova traduce o genera el MOD, vuelve a escribir esos archivos
(solo si cambian) y borra los de idiomas que ya no existen. Quitar LinguaNova del
juego borra también esta carpeta.

Comprobado con dos copias del mismo juego y una fuente solo latina: el paquete A
(ruso) y el B (español) se copiaron sobre un juego limpio, primero A y después B.
Con un Ren'Py simulado que ejecuta el bloque `init 999` real de `linguanova.rpy`,
el menú muestra los dos idiomas y el ruso sigue reemplazando la fuente sin
cirílico. Antes del cambio, ese mismo caso perdía la corrección del ruso (su texto
se habría visto con cuadros).

También se comprobó con Ren'Py 8.3.7 real (`renpy.sh <juego> lint`): con el
`linguanova.rpy` escrito para «spanish» copiado encima de un juego que ya tenía el
ruso, Ren'Py cargó los datos de los dos idiomas (`russian: Русский`,
`spanish: Español`) y el lint terminó sin errores.

## Traducciones que no hizo LinguaNova

Si la traducción de una carpeta la hizo otra persona (oficial o de fans) y LinguaNova solo
dejó ahí los datos del MOD, el paquete lleva únicamente los archivos `linguanova_*` de esa
carpeta, no la traducción ajena. Comprobado con la traducción oficial al español de «The
Question» (SDK de Ren'Py 8.3.7).
