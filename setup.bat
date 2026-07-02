@echo off
REM setup.bat - Cai dat 1 lan cho Windows. Nhap doi (double-click) hoac chay: setup.bat
cd /d "%~dp0"

echo ==================================================
echo   MEETING-AGENT - Cai dat (Windows)
echo ==================================================

where python >nul 2>nul
if errorlevel 1 (
  echo [X] Chua co Python. Cai tai: https://www.python.org/downloads/
  echo     Nho tick "Add Python to PATH" khi cai.
  pause
  exit /b 1
)
echo [OK] Python da co

where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo [i] ffmpeg se dung ban di kem (tu cai qua pip) - khong can lam gi them
) else (
  echo [OK] ffmpeg da co san trong may
)

echo -^> Tao moi truong Python (.venv) va cai thu vien...
python -m venv .venv
call .venv\Scripts\python -m pip install --quiet --upgrade pip
call .venv\Scripts\python -m pip install --quiet -r requirements.txt

echo.
echo [DONE] Cai dat xong!
echo    - Tiep theo: tao file key.json theo docs\01-tao-google-cloud.md, dat vao thu muc nay.
echo    - De dung: nhap doi "Chay tren Windows.bat" va chon trong menu.
pause
