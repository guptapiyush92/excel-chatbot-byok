@echo off
REM Excel Chatbot - Streamlit Version Launcher (Windows)

echo ================================================
echo   Starting Excel Chatbot (Streamlit)
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

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

echo Starting Streamlit server...
echo    URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo.

REM Run Streamlit
streamlit run ui\chatbot_byok_ui.py
