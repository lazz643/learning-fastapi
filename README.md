# FastAPI dengan Supabase dan GraphQL - Panduan Pemula

Proyek ini adalah contoh sederhana yang menunjukkan cara mengintegrasikan:
- **FastAPI**: Framework web Python yang cepat dan modern
- **Supabase**: "Firebase alternatif" open source yang menyediakan database dan autentikasi
- **GraphQL**: API query language untuk meminta data yang tepat sesuai kebutuhan

## 🚀 Cara Memulai (Langkah-demi-Langkah)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/learning-fastapi.git
cd learning-fastapi
```

### 2️⃣ Setup Lingkungan Python

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk Windows:
venv\Scripts\activate
# Untuk MacOS/Linux:
source venv/bin/activate

# Install semua package yang diperlukan
pip install -r backend/requirements.txt
```

### 3️⃣ Setup Supabase (Penting!)

1. Daftar akun gratis di [Supabase](https://supabase.com)
2. Buat project baru
3. Di dashboard project, dapatkan:
   - **URL**: Project URL (misalnya: https://abcdefghijk.supabase.co)
   - **API Key**: Anon/public key (dimulai dengan "eyJ...")

### 4️⃣ Buat File `.env`

Buat file bernama `.env` di folder `backend/` dengan isi:

```
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# JWT Authentication
SECRET_KEY=generate-a-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Catatan**: Ganti nilai-nilai di atas dengan kredensial Supabase Anda. Untuk `SECRET_KEY`, 
> gunakan string acak. Lihat `backend/ENV_TEMPLATE.md` untuk cara menghasilkan secret key.

### 5️⃣ Buat Tabel di Supabase

Di dashboard Supabase:
1. Pilih tab "Table Editor"
2. Klik "Create a new table"
3. Buat tabel bernama "products" dengan kolom:
   - `id` (type: int8, primary key, is identity: true)
   - `name` (type: text)
   - `description` (type: text)
   - `price` (type: int4)
   - `stock` (type: int4)
   - `created_at` (type: timestamptz, default: now())
   - `updated_at` (type: timestamptz, default: now())

4. Buat tabel bernama "purchases" dengan kolom:
   - `id` (type: int8, primary key, is identity: true)
   - `user_id` (type: int8, foreign key ke users.id)
   - `product_id` (type: int8, foreign key ke products.id)
   - `quantity` (type: int4)
   - `total_price` (type: int4)
   - `status` (type: text, default: 'pending')
   - `created_at` (type: timestamptz, default: now())
   - `updated_at` (type: timestamptz, default: now())

### 6️⃣ Jalankan Aplikasi

```bash
cd backend
uvicorn app.main:app --reload
```

### 7️⃣ Test Aplikasi

- **Test koneksi Supabase**: `python test_supabase.py`
- **Akses GraphQL Playground**: Buka http://localhost:8000/graphql di browser

## 📚 Apa yang Bisa Anda Lakukan?

### Contoh Query GraphQL

Dapatkan semua produk:
```graphql
query {
  products {
    id
    name
    price
    stock
  }
}
```

Tambah produk baru:
```graphql
mutation {
  createProduct(
    product: {
      name: "Smartphone",
      description: "Smartphone terbaru",
      price: 5000000,
      stock: 10
    }
  ) {
    id
    name
  }
}
```

Membuat pembelian baru (memerlukan login):
```graphql
mutation {
  createPurchase(
    purchase: {
      product_id: 1,
      quantity: 2
    },
    user_id: 1
  ) {
    id
    product_id
    quantity
    total_price
    status
  }
}
```

Melihat semua pembelian pengguna:
```graphql
query {
  userPurchases(user_id: 1) {
    id
    product_id
    quantity
    total_price
    status
    created_at
  }
}
```

## 📁 Struktur Proyek (Penjelasan Singkat)

```
learning-fastapi/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point aplikasi (mulai dari sini)
│   │   ├── supabase_client.py   # Koneksi ke Supabase
│   │   ├── graphql_schema.py    # Definisi tipe dan operasi GraphQL
│   │   └── ... (file lainnya)
│   ├── test_supabase.py         # Skrip untuk test koneksi Supabase
│   ├── requirements.txt         # Package Python yang dibutuhkan
│   └── DOCUMENTATION.md         # Dokumentasi teknis lengkap
└── README.md                    # Panduan yang sedang Anda baca ini
```

## 🔍 Ingin Mempelajari Lebih Lanjut?

- Dokumentasi lengkap: Lihat file `backend/DOCUMENTATION.md`
- Penjelasan kode: Setiap file kode memiliki komentar untuk membantu Anda memahami
- Tutorial video: [Coming soon]

## 🐛 Masalah Umum

- **Error "Connection failed" saat test Supabase**: Periksa SUPABASE_URL dan SUPABASE_KEY di file .env
- **Table not found error**: Pastikan Anda sudah membuat tabel "products" dan "purchases" di Supabase
- **Module not found**: Pastikan Anda sudah menginstall semua dependensi dengan `pip install -r requirements.txt`
- **Auth error pada endpoint pembelian**: Pastikan Anda sudah login dan menggunakan token JWT yang valid

## 📝 Lisensi

Proyek ini bersifat open source dan tersedia untuk tujuan pembelajaran. 