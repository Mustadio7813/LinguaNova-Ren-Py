# Aligerar el juego — revisión 2026-11-11_ALIGERAR_JUEGO

Herramienta nueva de **Utilidades** (modo avanzado). Crea una **copia más liviana** del juego Ren'Py abierto, con las imágenes, el audio y el vídeo recomprimidos. Procede del *Optimizador Ren'Py v3* del mismo autor, integrado sin consola: el avance se ve en la tarjeta, la tarea se puede detener y el resultado queda en un informe.

## Dónde está

**Utilidades → Aligerar el juego**, justo debajo de «Compartir o respaldar traducciones». Utilidades solo aparece con el modo avanzado activado (Ajustes). La tarjeta se bloquea mientras se traduce o se genera el MOD.

## Qué hace cada control

| Control | Efecto |
| --- | --- |
| Compresión: **Segura** | Sin ninguna pérdida: PNG con oxipng, JPEG con mozjpeg sin pérdida y WebP sin pérdida. El vídeo no se toca. |
| Compresión: **Equilibrada** (recomendada) | Pérdida imperceptible: PNG con paleta de calidad 85–98, JPEG 88, WebP 88, Opus 48 kb/s por canal y vídeo con el mismo códec. |
| Compresión: **Máxima** | El menor tamaño: puede notarse en degradados de color y en la música con auriculares. |
| Modo PC antiguo | Solo vídeos: como máximo 720p y 30 fps, VP9/AV1 → VP8 (webm/mkv) o H.264 (mp4). Se acepta aunque el vídeo pese algo más. No se recomienda para una copia que se vaya a compartir. |
| Quitar el motor para Linux y Mac | Borra en la copia `lib/*linux*`, `lib/*mac*`/`darwin`, los `.sh` y los `.app`. |
| Ajustes para PC con poca RAM | Añade `game/zz_gama_baja.rpy` (rollback 32, caché de imágenes de 150 MB). Se puede borrar si da problemas. |
| **Calcular ahorro** | Comprime una muestra (40 imágenes, 15 audios y 20 s de 2 vídeos) en una carpeta temporal. No escribe nada en el juego. |
| **Crear copia optimizada** | Pide la carpeta donde crear `<juego>_Optimizado` (por defecto, junto al juego) y crea la copia. |
| Detener | Detiene la tarea, incluido ffmpeg. La copia a medias se borra; una copia anterior completa se conserva. |
| Abrir copia | Abre la carpeta de la última copia creada. |

## Reglas que se mantienen del optimizador

- El juego original nunca se escribe. La copia se construye en `<destino>.parcial` y solo sustituye a una copia anterior al final.
- No se cambia la extensión de ningún archivo; los scripts siguen encontrando sus recursos.
- Un archivo solo se sustituye si el resultado es más pequeño (o más fácil de reproducir en el modo PC antiguo) y dura lo mismo.
- Ante un error en un archivo, ese archivo se deja como estaba y se anota en el informe.
- Los `.rpa` se extraen dentro de la copia (sin sobrescribir archivos sueltos, igual que la prioridad de Ren'Py) y se optimiza su contenido. Si un `.rpa` no se puede leer, se copia tal cual.
- Los `.rpyc` se conservan: las partidas guardadas siguen funcionando.
- No se copian `saves/`, `cache/`, los registros de la raíz (`log.txt`, `errors.txt`, `traceback.txt`) ni `.linguanova_backups/` (los respaldos de LinguaNova se quedan con el juego original).
- Motores Ren'Py antiguos (sin `lib/py3*` o con versión < 8): los `.ogg` se recomprimen como Vorbis, no como Opus.

## Cuándo usarlo

Después de traducir y generar el MOD. La copia lleva `game/tl/`, el MOD, el glosario y las fuentes tal como están en el juego; el informe de compartir traducciones y la copia optimizada son independientes.

## Informe

Al terminar se escribe `<destino>_informe.txt` junto a la copia, en el idioma de la interfaz: tamaño original y final, ahorro por sección, motor quitado, avisos (sin ffmpeg, motor antiguo, modo PC antiguo, poca RAM, `.rpa` conservados) y la lista de archivos que se dejaron igual por un problema.

## ffmpeg: un programa aparte

El audio y el vídeo necesitan **ffmpeg**. No es una librería de Python: LinguaNova lo **ejecuta** como un programa independiente (sin ventana de consola) y nunca lo importa. Sin ffmpeg solo se comprimen las imágenes y la tarjeta lo indica.

LinguaNova lo busca en este orden:

1. Junto al programa: `ffmpeg\ffmpeg.exe`, `ffmpeg.exe` o `bin\ffmpeg.exe` al lado del `.exe` (o del `.py` al ejecutar desde el código).
2. La carpeta de herramientas del usuario: `%LOCALAPPDATA%\LinguaNova\herramientas\ffmpeg\ffmpeg.exe` (compartida por todas las versiones de LinguaNova).
3. El archivo elegido con **Elegir ffmpeg.exe…** (se comprueba ejecutándolo y se recuerda en `ruta_elegida.txt` de esa carpeta).
4. El `PATH` de Windows.

| Versión | ffmpeg |
| --- | --- |
| **Portable** (`COMPILAR_PORTABLE.bat`, un solo EXE) | **No lo incluye**, para que el EXE siga siendo liviano y abra rápido. La tarjeta ofrece **Descargar ffmpeg (~100 MB)** la primera vez, o elegir un `ffmpeg.exe` que el usuario ya tenga. |
| **Instalable / en carpeta** (`COMPILAR.bat`) | **Lo incluye** en `dist\<programa>\ffmpeg\`. El BAT lo copia de `recursos\ffmpeg\ffmpeg.exe` si existe (compilación sin Internet) o lo descarga con el mismo procedimiento verificado. Si la descarga falla, el EXE funciona igual y lo ofrecerá al usarlo. |
| Desde el código (`INICIAR.bat`) | Igual que la portable: se busca, se descarga o se elige. |

### Descarga verificada

- Origen: compilación oficial *release essentials* de [www.gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (GPL v3). Si el archivo principal no responde, se prueba la réplica de GitHub de esa misma versión (`GyanD/codexffmpeg`).
- Antes de usarlo se comprueba la huella **SHA-256** publicada en `ffmpeg-release-essentials.zip.sha256`; si no coincide, el archivo se descarta.
- Solo se extraen `bin/ffmpeg.exe` y la licencia (`LICENSE_ffmpeg.txt`), y se prueba `ffmpeg -version`.
- Se escribe `ORIGEN.txt` con la URL, la huella, la fecha, la licencia y dónde obtener el código fuente.
- La descarga automática es solo para Windows. En otros sistemas se usa el ffmpeg del gestor de paquetes.

## Librerías de imagen (opcionales)

`LN_OPTIONAL_DEPENDENCIES`: `pillow`, `pyoxipng`, `imagequant` y `mozjpeg-lossless-optimization`. Se instalan aparte de las dependencias principales (`LN_start__ensure_optional`):

- solo paquetes ya compilados (`--only-binary :all:`), con pocos reintentos;
- si fallan (sin Internet o un Python sin paquetes para ellas), LinguaNova abre igual, la tarjeta dice qué falta y se reintenta como mucho una vez al día;
- el entorno principal **no** se reconstruye: la huella de `LN_DEPENDENCIES` no cambia.

Sin Pillow no se tratan imágenes; sin las otras tres se usa lo que haya (Pillow solo, PNG sin paleta, JPEG sin mozjpeg). En los EXE se incluyen si estaban instaladas al compilar (`--hidden-import` en los dos BAT).

## Rendimiento

Las imágenes se procesan en procesos aparte (`spawn`, hasta 4), porque oxipng y libimagequant no liberan el GIL. Si los procesos no se pueden crear, se hace lo mismo con hilos. El audio usa hasta 6 hilos y el vídeo va de uno en uno (es lo más lento). El arranque ya llama a `multiprocessing.freeze_support()`, necesario en los EXE.

## Licencias

LinguaNova es GPL v3, compatible con todos los componentes nuevos. `imagequant` (libimagequant) es GPL v3; ffmpeg de gyan.dev es GPL v3 y se distribuye como programa aparte con su licencia y el enlace al código fuente. Detalle en `THIRD_PARTY_NOTICES.md`.

## Código

| Pieza | Dónde (`LinguaNova_Traductor_RenPy.py`) |
| --- | --- |
| Optimizador | Módulo `src/tools/game_optimizer.py`, prefijo `LN_src_tools_game_optimizer__` (antes del punto de entrada). Funciones principales: `compress`, `estimate`, `find_ffmpeg`, `download_ffmpeg`, `remember_ffmpeg`. |
| Backend QML | Módulo `src/backend/optimizer_backend.py`, clase `LN_src_backend_optimizer_backend__OptimizerBackend`, publicada como `optimizerBackend`. Se detiene al cerrar la ventana. |
| Tarjeta | Recurso `src/gui/qml/components/OptimizeGameCard.qml`, registrado en `qmldir` y en `LN_RESOURCE_MAP`; usado en `Main.qml` debajo de `SharePackageCard`. |
| Textos | Claves `opt_*` en los cinco idiomas de la interfaz (es, en, fr, pt, ru). |
| Dependencias | `LN_OPTIONAL_DEPENDENCIES`, `LN_OPTIONAL_IMPORTS` y `LN_start__ensure_optional`. |
| Línea de órdenes | `--descargar-ffmpeg [carpeta]` (la usa `COMPILAR.bat`). |

No se integró la función *Desempaquetar* del optimizador (`.rpa` y `.rpyc` dentro del juego): LinguaNova ya lo hace con unrpa, su lector propio de RPA y el lector/descompilador de `.rpyc`.

## Pruebas

`docs/PRUEBA_ALIGERAR_JUEGO.py` abre la aplicación real en Qt sin pantalla con un juego de prueba (imágenes, audio, vídeo, un `.rpa` y motor de Linux) y usa la tarjeta como un usuario: 28 comprobaciones, aprobadas en las dos ediciones. Resultados en [RESULTADOS_PRUEBAS.md](RESULTADOS_PRUEBAS.md).

No se pudo probar en Windows: la compilación con PyInstaller, los procesos `spawn` dentro del EXE portable, la descarga real desde gyan.dev (se probó el mismo código con un servidor local y un archivo con huella correcta e incorrecta) y la carpeta `ffmpeg` dentro de `dist`.
