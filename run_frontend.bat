@echo off
echo ============================================
echo   Student Management Portal - Web Frontend
echo ============================================
echo.

REM Check if venv exists, if not create it
IF NOT EXIST "venv\Scripts\python.exe" (
    echo Creating virtual environment with Python 3.12...
    py -3.12 -m venv venv
    echo Installing requirements...
    venv\Scripts\pip.exe install flask
)

echo Starting the portal...
echo Open your browser at: http://localhost:5000
echo Press Ctrl+C to stop.
echo.
venv\Scripts\python.exe app.py
pause
