@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
if errorlevel 1 exit /b 1
set "APP_NAME=LinguaNova Traductor de Ren'Py"
set "TRIAL_SCRIPT=%~dp0LinguaNova_Traductor_RenPy.py"
set "TRIAL_PY="
set "TRIAL_PY_FILE=%~dp0.linguanova-python.txt"
set "TRIAL_LOG=%~dp0compilacion_error.log"
set "TRIAL_WORK=%~dp0build\prueba_155"
REM Build from code only. Never add config.json, AppData, .env or API keys.
REM Local environment overrides do not enter the compiler preparation process.
set "LINGUANOVA_DATA_DIR="
>"%TRIAL_LOG%" echo %APP_NAME% - Compilacion sin configuracion personal
if not exist "%TRIAL_SCRIPT%" (
    >>"%TRIAL_LOG%" echo [ERROR] Coloca el BAT junto a LinguaNova_Traductor_RenPy.py.
    goto fail
)
echo ============================================================
echo  %APP_NAME% - Compilacion: version en carpeta
echo ============================================================
echo.
echo Paso 1 de 3: preparando Python y las dependencias.
echo   La primera vez instala PyQt6 y otros componentes: puede tardar
echo   de 5 a 15 minutos y la ventana no mostrara mas texto mientras tanto.
echo   Mientras esta ventana siga abierta, el proceso continua.
echo   Detalle en vivo: compilacion_error.log
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto try_python
py -3 "%TRIAL_SCRIPT%" --preparar >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto fail
goto compile
:try_python
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    >>"%TRIAL_LOG%" echo [ERROR] Se necesita Python 3.10 o superior.
    goto fail
)
python "%TRIAL_SCRIPT%" --preparar >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto fail
:compile
if not exist "%TRIAL_PY_FILE%" (
    >>"%TRIAL_LOG%" echo [ERROR] Falta la ruta del Python preparado.
    goto fail
)
set /p "TRIAL_PY=" <"%TRIAL_PY_FILE%"
if not defined TRIAL_PY (
    >>"%TRIAL_LOG%" echo [ERROR] La ruta del Python preparado esta vacia.
    goto fail
)
if not exist "%TRIAL_PY%" (
    >>"%TRIAL_LOG%" echo [ERROR] No se preparo el entorno de compilacion.
    goto fail
)
echo   Listo.
echo.
if not exist "%TRIAL_WORK%" mkdir "%TRIAL_WORK%"
if errorlevel 1 goto fail
echo Paso 2 de 3: comprobando PyInstaller...
"%TRIAL_PY%" -m pip install "pyinstaller>=6.16,<7" >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto fail
echo   Listo.
echo.
echo Paso 3 de 3: compilando la version en carpeta.
echo   Suele tardar de 2 a 10 minutos; la ventana no mostrara mas texto hasta terminar.
set "ICON_FILE=%~dp0recursos\linguanova.ico"
set "SPLASH_FILE=%~dp0recursos\linguanova_splash.png"
if not exist "%~dp0scripts\optional_pyinstaller_args.py" (
    >>"%TRIAL_LOG%" echo [ERROR] Falta scripts\optional_pyinstaller_args.py.
    goto fail
)
set "OPTIONAL_IMPORTS="
for /f "delims=" %%I in ('""%TRIAL_PY%" "%~dp0scripts\optional_pyinstaller_args.py""') do set "OPTIONAL_IMPORTS=%%I"
if not exist "%ICON_FILE%" (
    >>"%TRIAL_LOG%" echo [ERROR] Falta recursos\linguanova.ico junto al BAT.
    goto fail
)
rem Imagen de carga mientras el EXE se abre: necesita Tcl/Tk, incluido en el Python de python.org.
"%TRIAL_PY%" -c "import tkinter" >nul 2>&1
if errorlevel 1 goto compile_without_splash
if not exist "%SPLASH_FILE%" goto compile_without_splash
"%TRIAL_PY%" -m PyInstaller --noconfirm --clean --onedir --windowed --collect-data py3langid %OPTIONAL_IMPORTS% --icon "%ICON_FILE%" --splash "%SPLASH_FILE%" --name "%APP_NAME%" --specpath "%TRIAL_WORK%" --workpath "%TRIAL_WORK%\pyinstaller" --distpath "%~dp0dist" "%TRIAL_SCRIPT%" >>"%TRIAL_LOG%" 2>&1
goto compiled
:compile_without_splash
echo   (Este Python no incluye Tcl/Tk: el EXE se abrira sin la imagen de carga previa.)
"%TRIAL_PY%" -m PyInstaller --noconfirm --clean --onedir --windowed --collect-data py3langid %OPTIONAL_IMPORTS% --icon "%ICON_FILE%" --name "%APP_NAME%" --specpath "%TRIAL_WORK%" --workpath "%TRIAL_WORK%\pyinstaller" --distpath "%~dp0dist" "%TRIAL_SCRIPT%" >>"%TRIAL_LOG%" 2>&1
:compiled
if errorlevel 1 goto fail
if not exist "%~dp0dist\%APP_NAME%\%APP_NAME%.exe" (
    >>"%TRIAL_LOG%" echo [ERROR] No se genero el ejecutable.
    goto fail
)
echo.
echo Paso extra: ffmpeg para el audio y el video de "Aligerar el juego".
echo   Es un programa aparte con licencia GPL; va en la carpeta ffmpeg junto al EXE.
set "FFMPEG_DIR=%~dp0dist\%APP_NAME%\ffmpeg"
if not exist "%~dp0recursos\ffmpeg\ffmpeg.exe" goto ffmpeg_download
if not exist "%~dp0recursos\ffmpeg\LICENSE_ffmpeg.txt" goto ffmpeg_download
if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"
copy /y "%~dp0recursos\ffmpeg\ffmpeg.exe" "%FFMPEG_DIR%\ffmpeg.exe" >nul
copy /y "%~dp0recursos\ffmpeg\LICENSE_ffmpeg.txt" "%FFMPEG_DIR%\LICENSE_ffmpeg.txt" >nul
echo   Copiado desde recursos\ffmpeg.
goto ffmpeg_done
:ffmpeg_download
echo   Descargando la version oficial de www.gyan.dev, unos 100 MB...
"%TRIAL_PY%" "%TRIAL_SCRIPT%" --directo --descargar-ffmpeg "%FFMPEG_DIR%" >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto ffmpeg_failed
echo   Listo.
goto ffmpeg_done
:ffmpeg_failed
echo   [AVISO] No se pudo descargar ffmpeg. El EXE funciona igual y lo ofrecera
echo           la primera vez que se use "Aligerar el juego".
echo           Tambien puedes dejar ffmpeg.exe en recursos\ffmpeg y volver a compilar.
:ffmpeg_done
echo.
echo Listo: dist\%APP_NAME%\%APP_NAME%.exe
echo Distribuye solo la carpeta dist\%APP_NAME% completa.
echo No distribuyas config.json, AppData, .env ni tu carpeta de desarrollo.
echo El EXE usa un perfil de configuracion separado del archivo PY.
pause
exit /b 0
:fail
echo.
type "%TRIAL_LOG%"
echo.
echo No se pudo compilar. Revisa compilacion_error.log e inicio_error.log.
pause
exit /b 1
