# LinguaNova 1.5.5

[English](README.md) · **Español**

LinguaNova 1.5.5 traduce juegos de Ren'Py. Esta versión incluye un punto de
entrada Python autónomo y conserva la sintaxis de Ren'Py, las variables, los
marcadores y las etiquetas al crear archivos de idioma traducidos.

> [!WARNING]
> El programa escribe archivos de traducción dentro del juego seleccionado.
> Haz una copia de seguridad y prueba primero sobre una copia. No se garantiza
> la calidad de cada traducción ni la compatibilidad con todos los juegos y
> recorridos. Esta versión no usa OCR para traducir texto dentro de imágenes.

> [!IMPORTANT]
> LinguaNova es un trabajo modificado de mantenimiento independiente, basado
> en parte en RenLocalizer 2.8.19. No es una versión oficial de RenLocalizer
> ni está afiliado, respaldado o mantenido por sus autores originales.
>
> Proyecto original: https://github.com/Lord0fTurk/RenLocalizer
>
> Copyright original conservado: Copyright (C) 2025 RenLocalizer V2 Authors
>
> Licencia: GNU GPL v3 o posterior (**GPL-3.0-or-later**)
> Consulta [NOTICE.md](NOTICE.md), [UPSTREAM.md](UPSTREAM.md),
> [LICENSE_POLICY.md](LICENSE_POLICY.md) y
> [MODIFICATIONS_LINGUANOVA.md](MODIFICATIONS_LINGUANOVA.md).

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)
![Ren'Py](https://img.shields.io/badge/Ren'Py-7%20y%208-ffb86b?style=flat-square)
![Licencia](https://img.shields.io/badge/Licencia-GPL--3.0--or--later-111827?style=flat-square)

## Inicio rápido

1. Haz una copia de seguridad del juego de Ren'Py.
2. Descarga o clona este repositorio y extrae el contenido en una carpeta normal.
3. Instala Python 3.10 o posterior si todavía no está instalado.
4. En Windows, ejecuta `run.bat`. En Linux o macOS, ejecuta
   `python3 LinguaNova_Traductor_RenPy.py` (o `./LinguaNova.sh`).
5. Selecciona la carpeta o el ejecutable admitido, el idioma de origen y el de
   destino, y el motor. Inicia la traducción y revisa el resultado dentro del
   juego antes de compartirlo.

La primera ejecución desde el código puede crear un entorno aislado y descargar
dependencias. Para preparar el entorno y usar motores en línea se necesita
conexión a Internet.

## Funciones incluidas

- Traducción de Ren'Py con protección de variables, marcadores y etiquetas.
- Análisis de archivos `.rpy`, `.rpyc` y contenido empaquetado compatible.
- Revisión de traducciones y correcciones manuales.
- Herramientas MOD para traducir la interfaz y aplicar correcciones desde la app.
- Cola de trabajos, progreso, cancelación y recuperación de operaciones
  interrumpidas.
- Controles para la clave API de DeepL y motores de traducción incluidos.
- Interfaz en inglés, español, francés, portugués y ruso.
- Respaldos verificados fuera de la carpeta `game/` y un comando para recuperar
  los archivos de la última operación.

El flujo MOD es independiente de la traducción principal. Que la preparación
del texto termine no garantiza que el juego vaya a iniciar correctamente; la
aplicación informa textos pendientes y avisos de verificación.

## Cancelar y restaurar

Pulsa **Detener** una sola vez y espera a que la operación actual guarde y
termine la limpieza. No cierres el proceso mientras escribe archivos.

Para restaurar el respaldo verificado de la última operación:

```text
python LinguaNova_Traductor_RenPy.py --restaurar "CARPETA_DEL_JUEGO" --idioma spanish
```

Cierra el juego antes de restaurar. La recuperación comprueba la ruta registrada
y las huellas de los archivos; se niega a sobrescribir archivos modificados
después de la operación. Consulta la
[guía de 1.5.5](docs/LEEME_1_5_5.md) y las
[notas de recuperación](docs/ARREGLO_CANCELACION_1_5_5.md).

## DeepL

Selecciona DeepL en la página Traducción, introduce la clave API y pulsa
**Guardar**. La clave se guarda en la configuración local del usuario, no en el
código fuente ni dentro del ejecutable. Consulta las
[notas de DeepL y compilación](docs/ARREGLO_DEEPL_Y_COMPILACION_1_5_5.md).

## Código fuente y compilaciones

El código de la aplicación 1.5.5 está en
[`LinguaNova_Traductor_RenPy.py`](LinguaNova_Traductor_RenPy.py). La fuente
modular anterior y sus pruebas de regresión se conservan en el repositorio por
compatibilidad y mantenimiento; el lanzador de Windows y la compilación GUI
predeterminados usan el punto de entrada 1.5.5.

- Ejecutar desde el código en Windows: `run.bat`
- Compilar carpeta portable en Windows: `build_windows.bat`
- Crear instalador de Windows: `build_installer.bat` (requiere Inno Setup 6.5+)
- Compilar la fuente autónoma directamente en Windows: `COMPILAR_1_5_5.bat`
- Ayuda de la CLI: `python LinguaNova_Traductor_RenPy.py --cli --help`

El ZIP contiene informes históricos de pruebas de una compilación de ensayo;
no sustituyen la ejecución de las pruebas de este repositorio sobre esta misma
fuente. El ejecutable de Windows y el juego elegido deben probarse en sus
sistemas de destino. Consulta la [guía 1.5.5](docs/LEEME_1_5_5.md) para conocer
las limitaciones.

## Contribuciones y pruebas

La suite de compatibilidad modular se ejecuta con:

```bash
python -m pytest -q
```

La prueba de regresión de la fuente autónoma comprueba su sintaxis. Para
informar un problema, incluye la versión de Ren'Py, el registro correspondiente
y los pasos para reproducirlo; no adjuntes archivos de juegos protegidos.

## Licencia

LinguaNova se distribuye bajo **GNU GPL-3.0-or-later**. Consulta
[LICENSE](LICENSE), [COPYING](COPYING), [NOTICE.md](NOTICE.md) y
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). No se añade ninguna
restricción de uso no comercial.
