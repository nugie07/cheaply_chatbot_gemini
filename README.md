# 🍱 Cheaply Restaurant - Chatbot AI Order System

Aplikasi chatbot AI untuk pemesanan makanan di restoran Cheaply (All You Can Eat Style Jepang) menggunakan Python, Streamlit, Gemini AI, dan Supabase.

## 📋 Fitur

- 🤖 Chatbot AI interaktif menggunakan Gemini API dengan style mirip Gemini
- 👤 Login/Register untuk member
- 👁️ Mode Guest untuk melihat menu dan ketersediaan booking
- 📅 Sistem booking interaktif via chatbot dengan perhitungan tanggal relatif (besok, lusa, sabtu minggu depan, dll)
- 🍱 Sistem pemesanan makanan dengan ekstraksi menu otomatis
- 💾 Database Supabase untuk menyimpan data
- 📧 Email konfirmasi booking menggunakan SMTP Gmail
- 🎨 UI modern dengan Gemini-like styling dan Bootstrap CSS
- 🖼️ Menampilkan gambar menu dari database
- ⭐ Menu favourite dengan filter khusus
- 📊 Riwayat pesanan dan booking aktif dari database

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.11 (wajib)
- Akun Google (untuk Gemini API)
- Akun Supabase (untuk database)
- Akun Gmail (untuk email konfirmasi)

### Step 1: Clone atau Download Project

```bash
cd chatbot-order
```

### Step 2: Setup Virtual Environment

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

### Step 3: Setup API Keys dan Konfigurasi

#### 3.1. Buat File `.env`

Copy file `env.template` menjadi `.env`:

```bash
# Windows
copy env.template .env

# Linux/Mac
cp env.template .env
```

#### 3.2. Dapatkan Gemini API Key

1. Kunjungi: https://makersuite.google.com/app/apikey
2. Login dengan Google account
3. Klik "Create API Key"
4. Copy API key
5. Paste ke `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

#### 3.3. Setup Supabase

1. Buat akun di: https://supabase.com
2. Buat project baru
3. Buka **Settings** → **API**
4. Copy **Project URL** dan **anon/public key**
5. Paste ke `.env`:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

#### 3.4. Setup Database Tables

1. Buka Supabase Dashboard → **SQL Editor**
2. Copy paste isi file `create_tables.sql`
3. Klik **Run**
4. Pastikan semua tabel berhasil dibuat:
   - `Member`
   - `Menu` (dengan kolom `favourite` dan `gambar`)
   - `Promo`
   - `booking`
   - `Order`

#### 3.5. Insert Dummy Data

```bash
# Pastikan venv sudah aktif
python dummy_data.py
```

Script ini akan membuat:
- 5 Member (untuk login)
- 20 Menu (dengan kolom `favourite` dan `gambar`)
- 4 Promo
- 3 Sample Booking

#### 3.6. Setup Email Service (SMTP Gmail)

**PENTING:** Email service adalah **optional**. Aplikasi tetap berjalan tanpa email, tapi email konfirmasi tidak akan dikirim.

**Cara Setup:**

1. **Enable 2-Step Verification di Gmail**
   - Buka: https://myaccount.google.com/security
   - Aktifkan 2-Step Verification

2. **Buat App Password**
   - Buka: https://myaccount.google.com/apppasswords
   - Pilih app: "Mail"
   - Pilih device: "Other (Custom name)"
   - Masukkan nama: "Cheaply Restaurant"
   - Klik "Generate"
   - **COPY PASSWORD** (16 karakter, contoh: `wxsk hvcc jlem uuyo`)

3. **Update File `.env`**
   ```env
   MAIL_MAILER=smtp
   MAIL_HOST=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD="wxsk hvcc jlem uuyo"
   MAIL_ENCRYPTION=tls
   MAIL_FROM_ADDRESS=your_email@gmail.com
   MAIL_FROM_NAME="Cheaply Restaurant"
   ```

   **Catatan:**
   - `MAIL_USERNAME`: Email Gmail Anda
   - `MAIL_PASSWORD`: App Password yang sudah dibuat (dengan tanda kutip)
   - `MAIL_FROM_ADDRESS`: Sama dengan `MAIL_USERNAME`
   - `MAIL_FROM_NAME`: Nama pengirim (bisa diubah)

4. **Test Email**
   - Setelah setup, email akan otomatis dikirim saat booking berhasil dibuat
   - Cek console untuk log: `✅ Email konfirmasi berhasil dikirim ke [email]`
   - Jika email tidak muncul di inbox, cek folder **Spam/Junk**

### Step 4: Jalankan Aplikasi

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
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
├── config.py           # Konfigurasi aplikasi dan system prompt
├── email_service.py    # Service untuk mengirim email konfirmasi (SMTP Gmail)
├── dummy_data.py       # Script untuk membuat dummy data
├── create_tables.sql   # SQL script untuk create/drop semua tabel
├── requirements.txt    # Dependencies Python
├── env.template        # Template file .env
├── run.bat / run.sh    # Script untuk menjalankan aplikasi
├── setup_venv.bat/sh  # Script untuk setup virtual environment
├── .gitignore          # File yang di-ignore oleh git
└── README.md           # Dokumentasi
```

## 🎯 Flow Aplikasi

1. **Halaman Welcome**: 
   - User memilih "View as Guest" atau "Login"
   - Chatbot otomatis menyapa dengan greeting sesuai waktu (Pagi/Siang/Sore/Malam)

2. **Mode Guest**: 
   - Dapat menanyakan menu dan ketersediaan booking
   - Chatbot dapat merekomendasikan 5 waktu terbaik
   - **TIDAK dapat melakukan booking** (akan diarahkan untuk login)
   - Tombol "Login untuk Booking" tersedia untuk redirect ke halaman login

3. **Mode Member (Login)**:
   - Semua fitur guest
   - Dapat melakukan booking **interaktif via chatbot** (tidak ada form)
   - Chatbot menanyakan: tanggal, jam, jumlah tamu, menu secara bertahap
   - Dapat memesan makanan (menu tersimpan ke table Order)
   - Dapat melihat booking aktif dan riwayat pesanan
   - Email konfirmasi otomatis dikirim saat booking berhasil

4. **Fitur Booking Interaktif**:
   - Mendukung tanggal relatif: "besok", "lusa", "sabtu minggu depan", dll
   - Ekstraksi menu otomatis dari pesan user
   - Validasi dan konfirmasi sebelum menyimpan ke database
   - Menampilkan menu yang sudah dipesan di konfirmasi

5. **Konfirmasi**: 
   - Setelah booking/order, user mendapat konfirmasi dengan detail lengkap
   - Email konfirmasi dikirim otomatis (jika email service sudah setup)

## 🔑 Login Credentials (Dummy Data)

Setelah menjalankan `dummy_data.py`, Anda dapat login dengan:

- **Nomor HP**: 081234567890
- **Password**: budi123

Atau gunakan member lain yang sudah dibuat oleh script.

## 🛠️ Teknologi yang Digunakan

- **Python 3.11** - Bahasa pemrograman
- **Streamlit 1.31.0** - Framework untuk web app
- **Google Gemini AI** - AI untuk chatbot (gemini-2.0-flash)
- **Supabase** - Database PostgreSQL
- **SMTP Gmail** - Email service untuk konfirmasi booking
- **Bootstrap CSS** - Styling
- **Python-dotenv** - Environment variables management

## 📧 Email Service

Aplikasi menggunakan **SMTP Gmail** untuk mengirim email konfirmasi booking.

### Fitur Email:
- ✅ Template HTML yang responsive dan modern
- ✅ Informasi booking lengkap (ID, tanggal, waktu, jumlah tamu, menu)
- ✅ No-reply email (tidak bisa dibalas)
- ✅ Auto-send saat booking berhasil dibuat

### Troubleshooting Email:

1. **Email tidak terkirim**
   - Pastikan `MAIL_USERNAME` dan `MAIL_PASSWORD` sudah benar di `.env`
   - Pastikan menggunakan **App Password**, bukan password biasa
   - Cek console untuk error message

2. **Email masuk Spam**
   - Normal untuk email pertama kali
   - Setelah beberapa kali, Gmail akan mengenali sebagai email legitimate
   - Untuk production, setup SPF/DKIM records

3. **Authentication Error**
   - Pastikan 2-Step Verification sudah diaktifkan
   - Pastikan App Password sudah dibuat dengan benar
   - Pastikan App Password di `.env` menggunakan tanda kutip: `"password"`

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
   - Pastikan nama file adalah `.env` (bukan `env.txt`)

4. **Error: SUPABASE_URL/SUPABASE_KEY tidak ditemukan**
   - Pastikan file `.env` sudah diisi dengan URL dan Key dari Supabase
   - Pastikan menggunakan `anon/public` key, bukan `service_role` key

5. **Error: Table tidak ditemukan**
   - Pastikan sudah menjalankan `create_tables.sql` di Supabase SQL Editor
   - Pastikan nama tabel sesuai (case-sensitive)
   - Script akan drop dan create ulang semua tabel

6. **Error: Module not found**
   - Pastikan virtual environment sudah diaktifkan
   - Install dependencies: `pip install -r requirements.txt`
   - Restart Streamlit setelah install library baru

7. **Chatbot tidak merespons**
   - Cek koneksi internet
   - Pastikan Gemini API key valid
   - Cek quota API key di Google Cloud Console

8. **Error: Permission denied (Linux/Mac)**
   - Beri permission: `chmod +x setup_venv.sh run.sh`

9. **Email tidak terkirim**
   - Pastikan email service sudah di-setup di `.env`
   - Pastikan menggunakan App Password (bukan password biasa)
   - Cek console untuk error message
   - Email mungkin masuk folder Spam/Junk

10. **Booking tidak tersimpan**
   - Pastikan user sudah login (bukan guest mode)
   - Cek console untuk error message
   - Pastikan semua informasi booking lengkap (tanggal, jam, jumlah tamu)

11. **Menu tidak muncul di konfirmasi**
   - Pastikan menu yang disebutkan ada di database
   - Chatbot akan menanyakan menu spesifik jika user menyebut menu umum (contoh: "sushi")
   - Menu harus match dengan nama menu di database

## 📝 Catatan Penting

- **Environment Variables**: File `.env` tidak di-commit ke git (sudah di `.gitignore`)
- **Email Service**: Optional, aplikasi tetap berjalan tanpa email
- **Database**: Pastikan Supabase project aktif dan tabel sudah dibuat
- **API Keys**: Jangan share API keys ke publik
- **Virtual Environment**: Selalu aktifkan venv sebelum menjalankan aplikasi
- **Restart Streamlit**: Setelah install library baru, restart Streamlit

## 🔒 Security Notes

- File `.env` berisi informasi sensitif, jangan commit ke git
- `credentials.json` dan `token.json` (jika ada) tidak di-commit
- Gunakan App Password untuk Gmail, bukan password biasa
- Untuk production, gunakan environment variables yang aman

## 📄 License

Project ini dibuat untuk keperluan edukasi.

## 🙏 Credits

- Google Gemini AI untuk chatbot intelligence
- Supabase untuk database service
- Streamlit untuk web framework
- Bootstrap untuk UI styling
