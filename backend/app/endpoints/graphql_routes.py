"""
GRAPHQL ROUTES - Koneksi GraphQL dengan FastAPI

File ini menghubungkan schema GraphQL dengan FastAPI, membuat endpoint:
1. /graphql - API publik yang bisa diakses tanpa login
2. /graphql/protected - API yang memerlukan autentikasi JWT

Apa itu GraphQL Router?
-----------------------
GraphQLRouter adalah kelas dari Strawberry yang mengintegrasikan GraphQL
dengan FastAPI, menghasilkan endpoint yang bisa menerima query GraphQL.

Apa yang dilakukan file ini?
---------------------------
1. Membuat router GraphQL publik tanpa autentikasi
2. Membuat fungsi untuk memvalidasi JWT token
3. Membuat router GraphQL terproteksi yang memerlukan autentikasi
"""

from fastapi import Depends, HTTPException, status  # Utilitas FastAPI
from strawberry.fastapi import GraphQLRouter  # Untuk menghubungkan GraphQL dengan FastAPI
from app.graphql_schema import schema  # Skema GraphQL yang sudah didefinisikan
from app.auth import get_current_user  # Fungsi untuk validasi JWT

# ======= ROUTER GRAPHQL PUBLIK =======
# Router ini untuk endpoint /graphql yang bisa diakses tanpa autentikasi
# Berguna untuk operasi-operasi publik seperti melihat produk
graphql_app = GraphQLRouter(schema)

# ======= AUTENTIKASI UNTUK GRAPHQL =======
# Fungsi untuk mengecek apakah pengguna sudah login (terautentikasi)
async def get_context(request):
    """
    Fungsi untuk mendapatkan konteks autentikasi dari request.
    
    Cara kerjanya:
    1. Ambil token JWT dari header Authorization
    2. Validasi token menggunakan fungsi get_current_user
    3. Jika valid, tambahkan informasi user ke konteks GraphQL
    4. Jika tidak valid, kembalikan error 401 Unauthorized
    
    Context ini akan tersedia di resolver GraphQL yang memerlukan autentikasi.
    """
    try:
        # Ambil token dari header Authorization (format: "Bearer <token>")
        authorization = request.headers.get("Authorization")
        
        # Cek apakah header Authorization ada dan formatnya benar
        if authorization and authorization.startswith("Bearer "):
            # Ambil token dari header (hapus bagian "Bearer ")
            token = authorization.replace("Bearer ", "")
            
            # Validasi token dan dapatkan informasi user
            user = await get_current_user(token)
            
            # Kembalikan konteks dengan informasi user
            return {"user": user}
            
        # Jika header tidak ada atau formatnya salah, kembalikan error
        raise HTTPException(status_code=401)
    except:
        # Jika terjadi error dalam proses validasi, kembalikan error autentikasi
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ======= ROUTER GRAPHQL TERPROTEKSI =======
# Router ini untuk endpoint /graphql/protected yang memerlukan autentikasi
# Berguna untuk operasi-operasi yang memerlukan login, seperti membuat/mengedit produk
protected_graphql_app = GraphQLRouter(
    schema,  # Menggunakan skema GraphQL yang sama
    context_getter=get_context  # Dengan tambahan fungsi validasi token
) 