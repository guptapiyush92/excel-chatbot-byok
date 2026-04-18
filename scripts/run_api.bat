@echo off
REM Excel Chatbot - FastAPI Version Launcher (Windows)

echo ================================================
echo   Starting Excel Chatbot (FastAPI)
echo ================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    if not exist .venv (
        echo X Virtual environment not found!
        echo Please run: scripts\quick_setup.bat
        pause
        exit /b 1
    )
)

REM Activate virtual environment
if exist venv (
    call venv\Scripts\activate.bat
) else (
    call .venv\Scripts\activate.bat
)

REM Check if FastAPI is installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

REM Set environment variables
if not defined API_HOST set API_HOST=0.0.0.0
if not defined API_PORT set API_PORT=8000

echo Starting FastAPI server...
echo    URL: http://localhost:%API_PORT%
echo.
echo Press Ctrl+C to stop
echo.

REM Run with uvicorn
python -m uvicorn api.main:app --host %API_HOST% --port %API_PORT% --reload
