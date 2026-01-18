-- ============================================
-- RECREATE ALL TABLES - Cheaply Restaurant
-- ============================================
-- PERINGATAN: Script ini akan MENGHAPUS semua data yang ada!
-- Semua tabel akan di-drop dan dibuat ulang dari awal
-- Jalankan script ini di Supabase SQL Editor

-- ============================================
-- STEP 1: DROP SEMUA TABLE (HAPUS DATA)
-- ============================================
-- Drop dalam urutan yang benar untuk menghindari foreign key constraint error
DROP TABLE IF EXISTS "Order" CASCADE;
DROP TABLE IF EXISTS "booking" CASCADE;
DROP TABLE IF EXISTS "Promo" CASCADE;
DROP TABLE IF EXISTS "Menu" CASCADE;
DROP TABLE IF EXISTS "Member" CASCADE;

-- ============================================
-- STEP 2: CREATE TABLE BARU
-- ============================================

-- Table Member
CREATE TABLE "Member" (
    id SERIAL PRIMARY KEY,
    "Nama Member" VARCHAR(255) NOT NULL,
    "Nomer Hp" VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table Menu
CREATE TABLE "Menu" (
    id SERIAL PRIMARY KEY,
    "Nama Menu" VARCHAR(255) NOT NULL,
    stock INTEGER DEFAULT 0,
    "Tipe" VARCHAR(100),
    "Harga" INTEGER NOT NULL,
    favourite BOOLEAN DEFAULT FALSE,
    gambar VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table Promo
CREATE TABLE "Promo" (
    id SERIAL PRIMARY KEY,
    "Nama Promo" VARCHAR(255) NOT NULL,
    "Menu" INTEGER REFERENCES "Menu"(id),
    "Harga Promo" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table booking
CREATE TABLE "booking" (
    id SERIAL PRIMARY KEY,
    "Id_member" INTEGER REFERENCES "Member"(id),
    tanggal_kedatangan DATE NOT NULL,
    jam_kedatangan VARCHAR(10) NOT NULL,
    jumlah_tamu INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table Order
CREATE TABLE "Order" (
    id SERIAL PRIMARY KEY,
    id_member INTEGER REFERENCES "Member"(id),
    id_booking INTEGER REFERENCES "booking"(id),
    menu INTEGER REFERENCES "Menu"(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- STEP 3: CREATE INDEX untuk performa
-- ============================================
CREATE INDEX idx_member_phone ON "Member"("Nomer Hp");
CREATE INDEX idx_booking_date ON "booking"(tanggal_kedatangan);
CREATE INDEX idx_order_member ON "Order"(id_member);
CREATE INDEX idx_order_booking ON "Order"(id_booking);
CREATE INDEX idx_menu_favourite ON "Menu"(favourite);

-- ============================================
-- SELESAI!
-- ============================================
-- Setelah script ini dijalankan:
-- 1. Jalankan dummy_data.py untuk insert data awal
-- 2. python dummy_data.py

