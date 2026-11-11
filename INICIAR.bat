@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto python
py -3 "%~dp0LinguaNova_Traductor_RenPy.py" %*
goto result
:python
python "%~dp0LinguaNova_Traductor_RenPy.py" %*
:result
set "TRIAL_EXIT=%ERRORLEVEL%"
if not "%TRIAL_EXIT%"=="0" pause
exit /b %TRIAL_EXIT%
