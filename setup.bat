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
  echo [!] Chua co ffmpeg. Cai bang:  winget install Gyan.FFmpeg
  echo     Cai xong mo lai cua so nay va chay lai setup.bat
) else (
  echo [OK] ffmpeg da co
)

echo -^> Tao moi truong Python (.venv) va cai thu vien...
python -m venv .venv
call .venv\Scripts\python -m pip install --quiet --upgrade pip
call .venv\Scripts\python -m pip install --quiet -r requirements.txt

echo.
echo [DONE] Xong! Cac buoc tiep theo:
echo    1) Tao file key.json theo docs\01-tao-google-cloud.md, dat vao thu muc nay.
echo    2) Boc bang:   .venv\Scripts\python transcribe.py "file-ghi-am.m4a"
echo    3) Dung Word:  .venv\Scripts\python make_bienban.py bienban.md
pause
