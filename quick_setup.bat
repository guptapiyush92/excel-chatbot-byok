@echo off
REM Quick Setup Script for Excel Chatbot (Windows)
REM This script automates the setup process

echo ================================================
echo   Excel Chatbot - Automated Setup (Windows)
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo Then run this script again.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo X Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q

REM Install requirements
echo Installing dependencies (this may take 5-10 minutes)...
echo Please wait...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    echo.
    echo Troubleshooting:
    echo - Check your internet connection
    echo - Try running as Administrator
    echo - Try: pip install --user -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [OK] All dependencies installed successfully!
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo [OK] .env file created. Edit it to add your API keys if using proxy mode.
    echo.
)

echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To run the application:
echo.
echo   BYOK Mode (users provide their own keys):
echo     venv\Scripts\activate
echo     streamlit run ui/chatbot_byok_ui.py
echo.
echo   Proxy Mode (you provide the key):
echo     venv\Scripts\activate
echo     streamlit run ui/chatbot_upload_ui.py
echo.
echo Then open http://localhost:8501 in your browser
echo.
echo ================================================
echo.
pause
