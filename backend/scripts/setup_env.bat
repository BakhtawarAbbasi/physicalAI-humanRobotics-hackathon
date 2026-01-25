@echo off
REM Setup script for RAG system on Windows

echo Setting up RAG system environment...

REM Check if Python 3.11+ is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python 3.11 or higher.
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set version=%%i
for /f "tokens=1,2,3 delims=." %%a in ("%version%") do (
    set major=%%a
    set minor=%%b
)

if %major% lss 3 (
    echo Python 3.11 or higher is required. Current version: %version%
    exit /b 1
)

if %major% equ 3 if %minor% lss 11 (
    echo Python 3.11 or higher is required. Current version: %version%
    exit /b 1
)

echo Python version %version% is compatible.

REM Install uv package manager if not already installed
pip list | findstr uv >nul 2>&1
if errorlevel 1 (
    echo Installing uv package manager...
    pip install uv
)

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    uv venv
)

REM Activate virtual environment and install dependencies
call .venv\Scripts\activate.bat
echo Installing dependencies...
uv pip install -e .

echo.
echo Environment setup complete!
echo To activate the virtual environment in the future, run: .venv\Scripts\activate.bat
echo.
echo Set your environment variables in .env file:
echo - COHERE_API_KEY=your_cohere_api_key
echo - QDRANT_URL=your_qdrant_cluster_url
echo - QDRANT_API_KEY=your_qdrant_api_key
echo.
echo Then run the ingestion pipeline with:
echo python cli.py --urls https://example.com/docs