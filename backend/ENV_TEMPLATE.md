# Template untuk File .env

Salin konten di bawah ini ke file `.env` baru di folder `backend/`:

```
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# JWT Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Database configuration (jika menggunakan SQLAlchemy)
# DB_USERNAME=username
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_NAME=mydatabase
# DB_PORT=3306
```

## Catatan Penting

1. File `.env` berisi informasi sensitif dan TIDAK disertakan dalam repositori Git.
2. Setiap kali Anda melakukan clone proyek ini, Anda HARUS membuat file `.env` Anda sendiri.
3. Dapatkan kredensial Supabase Anda dari dashboard Supabase di [https://app.supabase.com](https://app.supabase.com).
4. Untuk `SECRET_KEY`, gunakan string acak yang aman, misalnya dengan menjalankan perintah Python berikut:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ``` 