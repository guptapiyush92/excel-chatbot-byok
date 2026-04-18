@echo off
REM Run FastAPI Application (Windows)

echo ================================================
echo   Starting Excel Chatbot FastAPI Server
echo ================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo X Virtual environment not found!
    echo Please run: quick_setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if FastAPI is installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing FastAPI requirements...
    pip install -r requirements-api.txt
)

REM Set environment variables
if not defined API_HOST set API_HOST=0.0.0.0
if not defined API_PORT set API_PORT=8000

echo Starting server...
echo    URL: http://localhost:%API_PORT%
echo.
echo Press Ctrl+C to stop
echo.

REM Run with uvicorn
cd api
python -m uvicorn main:app --host %API_HOST% --port %API_PORT% --reload
