@echo off
setlocal

:: Get the path of the current virtual environment (if any)
set "venv_path=./.venv"

if exist "%venv_path%" (
    set "venv_py_path=%venv_path%\Scripts\python.exe"
    for /f "delims=" %%V in ('where python') do (
        if /I not "%%V"=="%venv_py_path%" (
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