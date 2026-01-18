@echo off
echo ========================================
echo Setup Virtual Environment - Cheaply Restaurant
echo ========================================
echo.

REM Check if Python 3.11 is available
python --version | findstr "3.11" >nul
if errorlevel 1 (
    echo [ERROR] Python 3.11 tidak ditemukan!
    echo Silakan install Python 3.11 terlebih dahulu.
    echo Download dari: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Membuat virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Gagal membuat virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment berhasil dibuat!

echo.
echo [2/4] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Gagal mengaktifkan virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment aktif!

echo.
echo [3/4] Upgrade pip...
python -m pip install --upgrade pip
echo [OK] Pip berhasil di-upgrade!

echo.
echo [4/4] Install dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Gagal install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies berhasil di-install!

echo.
echo ========================================
echo Setup selesai!
echo ========================================
echo.
echo Untuk mengaktifkan virtual environment di sesi berikutnya:
echo   venv\Scripts\activate.bat
echo.
echo Atau gunakan run.bat untuk langsung menjalankan aplikasi.
echo.
pause

