# LinguaNova 1.5.5 — primeros pasos

## Ejecutar

- **Windows:** ejecuta `run.bat`. Se necesita Python 3.10 o posterior.
- **Linux/macOS:** ejecuta `./LinguaNova.sh` o
  `python3 LinguaNova_Traductor_RenPy.py`.
- **CLI:** `python LinguaNova_Traductor_RenPy.py --cli --help`.

La primera ejecución desde el código puede preparar un entorno e instalar
dependencias; se requiere Internet para esa preparación.

## Traducir un juego

1. Cierra el juego y crea una copia de seguridad.
2. Selecciona la carpeta del juego o un ejecutable compatible de Ren'Py.
3. Elige idiomas y motor de traducción.
4. Inicia la traducción, espera a que el proceso termine y revisa los avisos.
5. Abre una copia del juego y comprueba los textos antes de compartirla.

Esta versión no traduce texto incrustado en imágenes mediante OCR. Los
resultados automáticos pueden necesitar revisión manual.

## Detener y restaurar

Pulsa **Detener** una vez y espera a que se guarde el progreso. Para restaurar
los archivos respaldados por la última operación:

```text
python LinguaNova_Traductor_RenPy.py --restaurar "RUTA_DEL_JUEGO" --idioma spanish
```

Cierra el juego antes de restaurar. La operación verifica rutas y archivos
antes de reemplazarlos; consulta [la guía 1.5.5](docs/LEEME_1_5_5.md).

## Archivos importantes

| Archivo | Función |
| --- | --- |
| `LinguaNova_Traductor_RenPy.py` | Aplicación autónoma 1.5.5. |
| `run.bat` | Lanzador de Windows para la versión 1.5.5. |
| `COMPILAR_1_5_5.bat` | Compilar la aplicación autónoma en Windows. |
| `build_windows.bat` | Compilar la distribución del repositorio con PyInstaller. |
| `build_installer.bat` | Crear instalador y paquete portable de Windows. |
| `pruebas.bat` | Ejecutar las pruebas del repositorio. |

LinguaNova se distribuye bajo GPL-3.0-or-later. Conserva los avisos de
[LICENSE](LICENSE), [NOTICE.md](NOTICE.md) y
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
