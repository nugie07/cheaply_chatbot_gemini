# 🍱 Cheaply Restaurant - Chatbot AI Order System

Aplikasi chatbot AI untuk pemesanan makanan di restoran Cheaply (All You Can Eat Style Jepang) menggunakan Python, Streamlit, Gemini AI, dan Supabase.

## 📋 Fitur

- 🤖 Chatbot AI interaktif menggunakan Gemini API
- 👤 Login/Register untuk member
- 👁️ Mode Guest untuk melihat menu dan ketersediaan
- 📅 Sistem booking dengan rekomendasi waktu
- 🍱 Sistem pemesanan makanan
- 💾 Database Supabase untuk menyimpan data
- 🎨 UI modern dengan Bootstrap CSS

## 🚀 Cara Install

### 1. Clone atau Download Project

```bash
cd chatbot-order
```

### 2. Setup Virtual Environment (Python 3.11)

**Windows:**
```bash
setup_venv.bat
```

**Linux/Mac:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

**Manual:**
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Catatan:** Pastikan menggunakan Python 3.11. Cek versi dengan `python --version`

### 3. Setup Environment Variables

Buat file `.env` di root project dengan isi:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

**Cara mendapatkan API Key:**
- Gemini API: https://makersuite.google.com/app/apikey
- Supabase: Buat project di https://supabase.com dan ambil URL dan API Key dari Settings > API

### 4. Setup Database Supabase

**PENTING:** Script ini akan menghapus semua data yang ada dan membuat ulang tabel!

1. Buka Supabase Dashboard: https://supabase.com/dashboard
2. Pilih project Anda
3. Buka **SQL Editor**
4. Copy paste isi file `create_tables.sql`
5. Klik **Run**

Script akan:
- Drop semua tabel yang ada (Order, booking, Promo, Menu, Member)
- Create ulang semua tabel dengan struktur terbaru
- Termasuk kolom `favourite` dan `gambar` di tabel Menu

### 5. Insert Dummy Data

Setelah tabel sudah dibuat, jalankan script untuk membuat dummy data:

```bash
python dummy_data.py
```

Script ini akan membuat:
- 5 Member (untuk login)
- 20 Menu (dengan kolom `favourite` dan `gambar`)
- 4 Promo
- 3 Sample Booking

## 🏃 Cara Menjalankan

**Pastikan virtual environment sudah diaktifkan terlebih dahulu!**

**Windows:**
```bash
# Aktifkan venv (jika belum)
venv\Scripts\activate

# Atau langsung jalankan
run.bat
```

**Linux/Mac:**
```bash
# Aktifkan venv (jika belum)
source venv/bin/activate

# Atau langsung jalankan
chmod +x run.sh
./run.sh
```

**Manual:**
```bash
# Aktifkan venv
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac

# Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📁 Struktur Project

```
chatbot-order/
├── app.py              # Aplikasi Streamlit utama
├── chatbot.py          # Class chatbot dengan Gemini AI
├── database.py         # Module untuk koneksi Supabase
├── config.py           # Konfigurasi aplikasi
├── dummy_data.py       # Script untuk membuat dummy data
├── create_tables.sql   # SQL script untuk create/drop semua tabel
├── requirements.txt    # Dependencies Python
├── env.template        # Template file .env
├── run.bat / run.sh    # Script untuk menjalankan aplikasi
├── setup_venv.bat/sh  # Script untuk setup virtual environment
└── README.md           # Dokumentasi
```

## 🎯 Flow Aplikasi

1. **Halaman Welcome**: User memilih "View as Guest" atau "Login"
2. **Mode Guest**: 
   - Dapat menanyakan menu dan ketersediaan
   - Chatbot dapat merekomendasikan 5 waktu terbaik
   - Tidak dapat melakukan booking
3. **Mode Member (Login)**:
   - Semua fitur guest
   - Dapat melakukan booking via chatbot atau form
   - Dapat memesan makanan
   - Dapat melihat konfirmasi booking dan order
4. **Konfirmasi**: Setelah booking/order, user dapat konfirmasi dan data tersimpan ke database

## 🔑 Login Credentials (Dummy Data)

Setelah menjalankan `dummy_data.py`, Anda dapat login dengan:

- **Nomor HP**: 081234567890
- **Password**: budi123

Atau gunakan member lain yang sudah dibuat oleh script.

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**
- **Streamlit** - Framework untuk web app
- **Google Gemini AI** - AI untuk chatbot
- **Supabase** - Database PostgreSQL
- **Bootstrap CSS** - Styling

## 📝 Catatan

- Pastikan koneksi internet aktif untuk menggunakan Gemini API
- Pastikan Supabase project sudah aktif dan tabel sudah dibuat
- Untuk production, gunakan environment variables yang aman

## 🐛 Troubleshooting

1. **Error: Python 3.11 tidak ditemukan**
   - Install Python 3.11 dari https://www.python.org/downloads/
   - Pastikan Python ditambahkan ke PATH
   - Cek dengan `python --version`

2. **Error: Virtual environment tidak ditemukan**
   - Jalankan `setup_venv.bat` (Windows) atau `./setup_venv.sh` (Linux/Mac)
   - Pastikan venv sudah dibuat sebelum menjalankan aplikasi

3. **Error: GEMINI_API_KEY tidak ditemukan**
   - Pastikan file `.env` sudah dibuat dan berisi API key yang valid

4. **Error: SUPABASE_URL/SUPABASE_KEY tidak ditemukan**
   - Pastikan file `.env` sudah diisi dengan URL dan Key dari Supabase

5. **Error: Table tidak ditemukan**
   - Pastikan sudah menjalankan `create_tables.sql` di Supabase SQL Editor
   - Pastikan nama tabel sesuai (case-sensitive)
   - Script akan drop dan create ulang semua tabel

6. **Error: Module not found**
   - Pastikan virtual environment sudah diaktifkan
   - Install dependencies: `pip install -r requirements.txt`

7. **Chatbot tidak merespons**
   - Cek koneksi internet
   - Pastikan Gemini API key valid
   - Cek quota API key di Google Cloud Console

8. **Error: Permission denied (Linux/Mac)**
   - Beri permission: `chmod +x setup_venv.sh run.sh`

## 📄 License

Project ini dibuat untuk keperluan edukasi.

