@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
if errorlevel 1 exit /b 1
set "APP_NAME=LinguaNova Traductor de Ren'Py"
set "TRIAL_SCRIPT=%~dp0LinguaNova_Traductor_RenPy.py"
set "TRIAL_PY=%~dp0.venv_prueba_155\Scripts\python.exe"
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
if not exist "%TRIAL_PY%" (
    >>"%TRIAL_LOG%" echo [ERROR] No se preparo el entorno de compilacion.
    goto fail
)
if not exist "%TRIAL_WORK%" mkdir "%TRIAL_WORK%"
if errorlevel 1 goto fail
echo Compilando. Esto puede tardar varios minutos...
"%TRIAL_PY%" -m pip install "pyinstaller>=6.16,<7" >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto fail
"%TRIAL_PY%" -m PyInstaller --noconfirm --clean --onedir --windowed --collect-data py3langid --name "%APP_NAME%" --specpath "%TRIAL_WORK%" --workpath "%TRIAL_WORK%\pyinstaller" --distpath "%~dp0dist" "%TRIAL_SCRIPT%" >>"%TRIAL_LOG%" 2>&1
if errorlevel 1 goto fail
if not exist "%~dp0dist\%APP_NAME%\%APP_NAME%.exe" (
    >>"%TRIAL_LOG%" echo [ERROR] No se genero el ejecutable.
    goto fail
)
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
