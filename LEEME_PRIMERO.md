<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Novedad: Aligerar el juego

Utilidades (modo avanzado) incluye **Aligerar el juego**, que crea una copia más liviana del juego. Para el audio y el vídeo usa **ffmpeg**, un programa aparte:

- **COMPILAR.bat** (versión en carpeta) lo incluye en `dist/…/ffmpeg/`: lo copia de `recursos/ffmpeg/ffmpeg.exe` si lo dejas ahí, o lo descarga.
- **COMPILAR_PORTABLE.bat** no lo incluye: el programa lo descarga la primera vez que se usa la herramienta, o se elige un `ffmpeg.exe`.

Detalle en `docs/ALIGERAR_JUEGO.md`.

---

# LinguaNova Traductor de Ren'Py 1.5.5

- Para iniciar desde el código fuente en Windows: **INICIAR.bat**.
- Para generar el ejecutable de Windows hay dos opciones:
  - **COMPILAR_PORTABLE.bat**: un solo archivo con todo dentro, `dist_portable/LinguaNova Traductor de Ren'Py.exe`. Se reparte tal cual; tarda unos segundos más en abrir.
  - **COMPILAR.bat**: carpeta `dist/LinguaNova Traductor de Ren'Py/`, con el `.exe` (pesa solo unos MB) y `_internal` (Qt y Python). Arranca al instante; se reparte la carpeta completa, incluida `_internal`.

Los dos usan el ícono de `recursos/linguanova.ico`; no borres la carpeta `recursos`.

Lee `docs/LEEME.md` y `docs/COMPILAR.md` para los detalles de uso y compilación.
El paquete contiene el código fuente; no incluye un EXE ya compilado.
