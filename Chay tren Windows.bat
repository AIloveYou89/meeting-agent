@echo off
REM Chay tren Windows.bat
REM  - Nhap doi (double-click) de hien menu.
REM  - HOAC keo tha 1 file ghi am len file nay -> boc bang luon.
chcp 65001 >nul
cd /d "%~dp0"
set "PY=.venv\Scripts\python.exe"

REM --- Lan dau: tu cai dat ---
if not exist "%PY%" (
  echo Lan dau chay - dang cai dat (mat 1-2 phut)...
  call setup.bat
  if not exist "%PY%" (
    echo.
    echo [X] Cai dat chua xong. Xem docs\02-cai-dat.md de cai Python truoc.
    pause
    exit /b 1
  )
)

REM --- Neu keo tha 1 file len icon -> boc bang file do luon ---
if not "%~1"=="" (
  "%PY%" transcribe.py "%~1"
  echo.
  pause
  exit /b
)

:menu
cls
echo ==================================================
echo    MEETING-AGENT
echo ==================================================
echo    1) Boc bang file ghi am   -^>  chu (transcript)
echo    2) Tao bien ban Word tu file bienban.md
echo    3) (nang cao) Day cong viec len Google Sheet Gantt
echo    4) Cai dat lai / cap nhat thu vien
echo    0) Thoat
echo --------------------------------------------------
set "choice="
set /p "choice=   Chon (1 / 2 / 3 / 4 / 0): "
echo.
if "%choice%"=="1" goto boc
if "%choice%"=="2" goto word
if "%choice%"=="3" goto gantt
if "%choice%"=="4" goto caidat
if "%choice%"=="0" exit /b
echo Chon khong hop le.
pause
goto menu

:boc
echo Keo file ghi am tha vao cua so nay roi Enter (hoac go duong dan):
set "f="
set /p "f=File: "
if not defined f ( echo Ban chua chon file. ) else ( "%PY%" transcribe.py %f% )
pause
goto menu

:word
echo Keo file bien ban .md vao day roi Enter (de trong = dung bienban.md):
set "f=bienban.md"
set /p "f=File: "
"%PY%" make_bienban.py %f%
pause
goto menu

:gantt
echo Keo file bien ban .md vao day roi Enter (de trong = dung bienban.md):
set "f=bienban.md"
set /p "f=File: "
echo Nhap ID Google Sheet Gantt (de trong neu da dat bien GANTT_SHEET_ID):
set "sid="
set /p "sid=Sheet ID: "
if defined sid ( "%PY%" push_to_gantt.py %f% --sheet %sid% ) else ( "%PY%" push_to_gantt.py %f% )
pause
goto menu

:caidat
call setup.bat
pause
goto menu
