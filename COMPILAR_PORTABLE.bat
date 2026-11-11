@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
if errorlevel 1 exit /b 1
set "APP_NAME=LinguaNova Traductor de Ren'Py"
set "TRIAL_SCRIPT=%~dp0LinguaNova_Traductor_RenPy.py"
set "TRIAL_PY="
set "TRIAL_PY_FILE=%~dp0.linguanova-python.txt"
set "TRIAL_LOG=%~dp0compilacion_portable_error.log"
set "TRIAL_WORK=%~dp0build\portable_155"
REM Build from code only. Never add config.json, AppData, .env or API keys.
REM Local environment overrides do not enter the compiler preparation process.
set "LINGUANOVA_DATA_DIR="
>"%TRIAL_LOG%" echo %APP_NAME% - Compilacion portable (un solo EXE) sin configuracion personal
if not exist "%TRIAL_SCRIPT%" (
    >>"%TRIAL_LOG%" echo [ERROR] Coloca el BAT junto a LinguaNova_Traductor_RenPy.py.
    goto fail
)
echo ============================================================
echo  %APP_NAME% - Compilacion: version portable (un solo EXE)
echo ============================================================
echo.
echo Paso 1 de 3: preparando Python y las dependencias.
echo   La primera vez instala PyQt6 y otros componentes: puede tardar
echo   de 5 a 15 minutos y la ventana no mostrara mas texto mientras tanto.
echo   Mientras esta ventana siga abierta, el proceso continua.
echo   Detalle en vivo: compilacion_portable_error.log
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
echo Paso 3 de 3: compilando la version portable (un solo EXE con todo dentro).
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
"%TRIAL_PY%" -m PyInstaller --noconfirm --clean --onefile --windowed --collect-data py3langid %OPTIONAL_IMPORTS% --icon "%ICON_FILE%" --splash "%SPLASH_FILE%" --name "%APP_NAME%" --specpath "%TRIAL_WORK%" --workpath "%TRIAL_WORK%\pyinstaller" --distpath "%~dp0dist_portable" "%TRIAL_SCRIPT%" >>"%TRIAL_LOG%" 2>&1
goto compiled
:compile_without_splash
echo   (Este Python no incluye Tcl/Tk: el EXE se abrira sin la imagen de carga previa.)
"%TRIAL_PY%" -m PyInstaller --noconfirm --clean --onefile --windowed --collect-data py3langid %OPTIONAL_IMPORTS% --icon "%ICON_FILE%" --name "%APP_NAME%" --specpath "%TRIAL_WORK%" --workpath "%TRIAL_WORK%\pyinstaller" --distpath "%~dp0dist_portable" "%TRIAL_SCRIPT%" >>"%TRIAL_LOG%" 2>&1
:compiled
if errorlevel 1 goto fail
if not exist "%~dp0dist_portable\%APP_NAME%.exe" (
    >>"%TRIAL_LOG%" echo [ERROR] No se genero el ejecutable.
    goto fail
)
echo.
echo Listo: dist_portable\%APP_NAME%.exe
echo Es un solo archivo con todo dentro: se reparte tal cual, sin carpeta _internal.
echo Al abrirlo tarda unos segundos mas, porque se descomprime en una carpeta temporal.
echo No distribuyas config.json, AppData, .env ni tu carpeta de desarrollo.
echo ffmpeg no va dentro del EXE portable para que siga siendo liviano: lo descarga
echo "Aligerar el juego" la primera vez que se usa, o el usuario elige un ffmpeg.exe.
echo El EXE usa un perfil de configuracion separado del archivo PY.
pause
exit /b 0
:fail
echo.
type "%TRIAL_LOG%"
echo.
echo No se pudo compilar. Revisa compilacion_portable_error.log e inicio_error.log.
pause
exit /b 1
