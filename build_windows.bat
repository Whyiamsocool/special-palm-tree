@echo off
REM Build script for creating WalletExporter.exe on Windows
REM Usage: build_windows.bat

echo ===================================
echo WalletExporter Windows Build Script
echo ===================================
echo.

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python not found in PATH
    echo Please install Python 3.11+ and add it to your PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

echo Checking Python version...
echo Found: Python %PYTHON_VERSION%

python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python 3.11+ required ^(found: %PYTHON_VERSION%^)
    pause
    exit /b 1
)

echo ✓ Python version OK
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Clean previous builds
if exist "dist" (
    echo Cleaning previous build artifacts...
    rmdir /s /q dist
    if exist "build" rmdir /s /q build
    echo ✓ Clean complete
    echo.
)

REM Run PyInstaller
echo Building WalletExporter.exe...
echo ^(This may take a minute or two...^)
echo.

pyinstaller WalletExporter.spec

if %errorlevel% neq 0 (
    echo ❌ ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo ===================================
echo ✓ Build Successful!
echo ===================================
echo.
echo Location: dist\WalletExporter\WalletExporter.exe
echo.
echo To run the application:
echo   dist\WalletExporter\WalletExporter.exe
echo.
echo Or navigate to dist\WalletExporter and double-click WalletExporter.exe
echo.
echo Note: Windows Defender SmartScreen may show a warning.
echo Click "More info" then "Run anyway" to proceed.
echo.
pause
