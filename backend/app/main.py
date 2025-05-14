"""
MAIN APPLICATION FILE - ENTRY POINT

File ini adalah titik masuk utama untuk aplikasi FastAPI kita.
Di sini kita mendefinisikan semua endpoint API dan mengatur konfigurasi aplikasi.

Apa itu FastAPI?
---------------
FastAPI adalah framework web modern untuk Python yang sangat cepat dan mudah digunakan.
Framework ini secara otomatis menghasilkan dokumentasi API interaktif (Swagger UI).

Struktur File:
------------
1. Import dan Konfigurasi: Mengimpor library dan mengatur logging
2. Inisialisasi Aplikasi: Membuat objek FastAPI dan mendaftarkan rute
3. API Endpoints: Mendefinisikan endpoint untuk operasi REST API
4. GraphQL Integration: Menghubungkan GraphQL dengan FastAPI

Teknologi yang Digunakan:
-----------------------
- FastAPI: Framework web utama
- SQLAlchemy: ORM (Object-Relational Mapping) untuk database relasional
- Supabase: Penyimpanan data cloud (digunakan oleh GraphQL)
- GraphQL: API query language alternatif untuk REST
"""

from fastapi import FastAPI, Depends, HTTPException  # Framework FastAPI
from sqlalchemy.orm import Session  # ORM untuk database SQL
from app.database import SessionLocal, engine  # Konfigurasi database
from app import models, schemas, crud, auth  # Modul aplikasi
from app.endpoints.graphql_routes import graphql_app, protected_graphql_app  # GraphQL routers
import logging  # Untuk logging

# ======= KONFIGURASI LOGGING =======
# Mengatur level log INFO agar kita bisa melihat proses penting yang terjadi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======= SETUP DATABASE =======
# Mencoba membuat tabel database berdasarkan model SQLAlchemy
# Ini hanya untuk kompatibilitas, aplikasi utamanya menggunakan Supabase
try:
    # Membuat tabel database jika belum ada
    models.Base.metadata.create_all(bind=engine)
    logger.info("SQLAlchemy models created")
except Exception as e:
    logger.warning(f"Could not create SQLAlchemy models: {e}")
    logger.info("Continuing without SQLAlchemy models - using Supabase only")

# ======= INISIALISASI APLIKASI FASTAPI =======
# Membuat objek FastAPI yang menjadi pusat dari aplikasi kita
app = FastAPI(
    title="FastAPI with Supabase and GraphQL",
    description="API untuk mengelola produk dan pengguna menggunakan GraphQL dan Supabase",
    version="1.0.0"
)

# ======= INTEGRASI GRAPHQL =======
# Mendaftarkan GraphQL endpoint ke aplikasi FastAPI
# Endpoint /graphql untuk akses publik
app.include_router(graphql_app, prefix="/graphql")
# Endpoint /graphql/protected memerlukan autentikasi
app.include_router(protected_graphql_app, prefix="/graphql/protected")

# ======= UTILITY FUNCTIONS =======
# Fungsi untuk mendapatkan sesi database untuk endpoint REST
def get_db():
    """
    Dependency untuk mendapatkan sesi database.
    Digunakan oleh endpoint REST untuk interaksi dengan database.
    """
    db = SessionLocal()
    try:
        yield db  # Memberikan sesi database ke endpoint
    finally:
        db.close()  # Pastikan sesi ditutup setelah selesai

# ======= API ENDPOINT SEDERHANA =======
# Endpoint root untuk health check
@app.get("/")
def read_root():
    """
    Endpoint root sederhana untuk memastikan API berjalan.
    Berguna untuk health check dan monitoring.
    """
    return {
        "status": "ok", 
        "message": "API is running. Use /graphql for GraphQL API",
        "docs": "/docs"  # Swagger UI documentation
    }

# ======= REST API ENDPOINTS (OPSIONAL) =======
# Endpoint berikut adalah alternatif REST API, tapi fokus utama aplikasi adalah GraphQL

@app.post("/register", response_model=schemas.UserResponse, tags=["Authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint untuk mendaftarkan pengguna baru.
    
    - Request body: Username, email, dan password
    - Returns: Data pengguna yang berhasil didaftarkan
    """
    try:
        # Cek apakah username sudah digunakan
        db_user = crud.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        # Buat pengguna baru
        return crud.create_user(db, user)
    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")

@app.post("/login", tags=["Authentication"])
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint untuk login pengguna.
    
    - Request body: Username dan password
    - Returns: Token akses untuk autentikasi
    """
    try:
        # Autentikasi pengguna
        user_db = crud.authenticate_user(db, user.username, user.password)
        if not user_db:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        # Buat token JWT
        access_token = auth.create_access_token(data={"sub": user_db.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")

@app.post("/products", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint untuk membuat produk baru.
    
    - Request body: Nama, deskripsi, harga, dan stok produk
    - Returns: Data produk yang berhasil dibuat
    """
    try:
        # Buat produk baru di database
        return crud.create_product(db, product)
    except Exception as e:
        logger.error(f"Error in create_product endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")