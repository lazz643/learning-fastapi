# FastAPI dengan Supabase dan GraphQL

Proyek ini mengintegrasikan FastAPI dengan Supabase sebagai backend dan GraphQL untuk API.

## Persiapan

1. Clone repository ini:
   ```
   git clone https://github.com/yourusername/learning-fastapi.git
   cd learning-fastapi
   ```

2. Setup environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # MacOS/Linux
   pip install -r backend/requirements.txt
   ```

3. **PENTING**: Buat file `.env` di folder `backend/`
   
   File `.env` berisi informasi sensitif dan tidak disertakan dalam repository. Anda perlu membuat file ini sendiri dengan format:
   ```
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_key_here
   
   # JWT Authentication
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   
   Lihat file `backend/ENV_TEMPLATE.md` untuk informasi lebih lanjut.

4. Jalankan aplikasi:
   ```
   cd backend
   uvicorn app.main:app --reload
   ```

5. Akses GraphQL Playground di: http://localhost:8000/graphql

## Dokumentasi

Dokumentasi lengkap dapat ditemukan di file `backend/DOCUMENTATION.md`.

## Fitur

- FastAPI sebagai framework web
- Supabase sebagai database/BaaS
- GraphQL untuk API
- Autentikasi JWT
- Manajemen produk (CRUD)

## Struktur Direktori

```
learning-fastapi/
├── backend/
│   ├── app/                     # Kode aplikasi utama
│   ├── test_supabase.py         # Script untuk test koneksi ke Supabase
│   ├── requirements.txt         # Dependensi Python
│   ├── ENV_TEMPLATE.md          # Template untuk file .env
│   └── DOCUMENTATION.md         # Dokumentasi lengkap
└── README.md                    # File ini
``` 