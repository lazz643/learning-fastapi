# Panduan Membuat File `.env`

## 🔐 Apa itu File `.env`?

File `.env` adalah file **rahasia** yang berisi *environment variables* (variabel lingkungan) seperti kredensial API, password, dan pengaturan rahasia lainnya. File ini **TIDAK** disimpan di Git/GitHub karena berisi informasi sensitif.

## 📋 Langkah-langkah

1. Buat file baru bernama **`.env`** (persis seperti ini, dengan titik di depan) di folder `backend/`
2. Salin kode di bawah ini ke dalam file tersebut
3. Ganti semua nilai contoh dengan nilai asli dari akun Supabase Anda

## 📝 Template

```env
# ===== KONFIGURASI SUPABASE =====
# URL dari project Supabase Anda
# Contoh: https://abcdefghijklm.supabase.co
SUPABASE_URL=your_supabase_url_here

# API Key Supabase (anon/public key)
# Dapatkan dari: Dashboard Supabase > Settings > API > Project API keys
# Contoh: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_KEY=your_supabase_anon_key

# ===== KONFIGURASI JWT =====
# Secret key untuk JWT (gunakan string acak yang aman)
# PENTING: Buat sendiri, jangan gunakan contoh ini!
SECRET_KEY=generate-random-secret-key

# Algoritma enkripsi untuk JWT (biarkan HS256)
ALGORITHM=HS256

# Masa berlaku token dalam menit
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ===== KONFIGURASI DATABASE (OPSIONAL) =====
# Bagian ini hanya diperlukan jika Anda menggunakan MySQL
# Jika hanya menggunakan Supabase, bisa dikomentar dengan #
# DB_USERNAME=username
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_NAME=mydatabase
# DB_PORT=3306
```

## ⚠️ Cara Membuat Secret Key yang Aman

Secret key adalah rahasia yang digunakan untuk enkripsi token JWT. Penting untuk menggunakan key yang acak dan aman.

Untuk membuat secret key yang aman, jalankan perintah Python berikut:

```python
import secrets
print(secrets.token_hex(32))
# Output contoh: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

## 🚨 Peringatan Penting

1. **JANGAN PERNAH** mengunggah file `.env` ke Git/GitHub!
2. **JANGAN PERNAH** membagikan isi file `.env` kepada orang lain!
3. Jika kredensial Anda terlanjur terekspos, segera ganti di dashboard Supabase.

## 🔄 Cara Setup untuk Lingkungan Berbeda

Untuk pengembangan di lingkungan berbeda, Anda bisa membuat beberapa file seperti:
- `.env.development` - untuk pengembangan lokal
- `.env.production` - untuk server produksi