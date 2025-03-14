@echo off
setlocal

:: Get the path of the current virtual environment (if any)
if defined VIRTUAL_ENV (
    for /f "delims=" %%V in ('where python') do (
        echo Checking: %%V
        if /I not "%%V"=="%VIRTUAL_ENV%\Scripts\python.exe" (
            echo Using: %%V
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
pause