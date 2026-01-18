#!/bin/bash

echo "========================================"
echo "Setup Virtual Environment - Cheaply Restaurant"
echo "========================================"
echo ""

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo "[ERROR] Python 3.11 tidak ditemukan!"
    echo "Silakan install Python 3.11 terlebih dahulu."
    echo "Download dari: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Membuat virtual environment..."
python3.11 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal membuat virtual environment!"
    exit 1
fi
echo "[OK] Virtual environment berhasil dibuat!"

echo ""
echo "[2/4] Mengaktifkan virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal mengaktifkan virtual environment!"
    exit 1
fi
echo "[OK] Virtual environment aktif!"

echo ""
echo "[3/4] Upgrade pip..."
python -m pip install --upgrade pip
echo "[OK] Pip berhasil di-upgrade!"

echo ""
echo "[4/4] Install dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal install dependencies!"
    exit 1
fi
echo "[OK] Dependencies berhasil di-install!"

echo ""
echo "========================================"
echo "Setup selesai!"
echo "========================================"
echo ""
echo "Untuk mengaktifkan virtual environment di sesi berikutnya:"
echo "  source venv/bin/activate"
echo ""
echo "Atau gunakan run.sh untuk langsung menjalankan aplikasi."
echo ""

