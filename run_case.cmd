@echo off
setlocal
set "python=%~dp0.venv\Scripts\python.exe"
if exist "%python%" (
    "%python%" -X utf8 "%~dp0run_case.py" %*
) else (
    py -3 -X utf8 "%~dp0run_case.py" %*
)
set "code=%errorlevel%"
if "%~1"=="" (
    echo.
    pause
)
exit /b %code%
