"""
File ini bertugas menghubungkan aplikasi ke Supabase.

Apa itu Supabase?
-----------------
Supabase adalah platform "Backend as a Service" (BaaS) open source, 
mirip dengan Firebase, tapi menggunakan PostgreSQL sebagai database.

Apa yang dilakukan file ini?
--------------------------
1. Mengimpor library yang diperlukan
2. Mengambil kredensial Supabase dari file .env
3. Membuat koneksi dengan Supabase

Cara penggunaan:
--------------
Setelah file ini dijalankan, Anda bisa menggunakan variabel 'supabase'
untuk berinteraksi dengan Supabase, contohnya:
- supabase.table("products").select("*").execute()
- supabase.table("users").insert({"username": "user1"}).execute()
"""

from supabase import create_client  # Library untuk koneksi ke Supabase
import os  # Untuk mengakses variabel lingkungan
from dotenv import load_dotenv  # Untuk memuat file .env

# Memuat variabel dari file .env
# File .env berisi kredensial yang tidak boleh disimpan di Git
load_dotenv()

# Mengambil kredensial Supabase dari variabel lingkungan
# URL Proyek Supabase (misal: https://abcdefghijk.supabase.co)
SUPABASE_URL = os.getenv("SUPABASE_URL")
# API Key Supabase (anon/public key, dimulai dengan "eyJ...")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inisialisasi klien Supabase dengan URL dan key
# Klien ini yang akan kita gunakan untuk semua interaksi dengan Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) 