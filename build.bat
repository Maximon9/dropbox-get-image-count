@echo off
setlocal

:: Get the path of the current virtual environment (if any)
set "venv_path=./.venv"

if exist "%venv_path%" (
    for /f "delims=" %%V in ('where python') do (
        if /I not "%%V"=="%venv_path%\Scripts\python.exe" (
            "%%V" build.py
            goto :end
        )
    )
) else (
    echo No virtual environment detected.
    python build.py
)

:end
endlocal
: exit
pause