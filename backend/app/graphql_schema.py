"""
File ini mendefinisikan skema GraphQL untuk API kita.

Apa itu GraphQL?
---------------
GraphQL adalah bahasa query untuk API. Tidak seperti REST API, dengan GraphQL,
klien dapat meminta data dengan tepat sesuai kebutuhan, tidak lebih dan tidak kurang.

Struktur File ini:
----------------
1. Tipe Data (User, Product): Mendefinisikan bentuk data yang tersedia
2. Input Types: Format data untuk operasi mutasi (create/update)
3. Query: Fungsi-fungsi untuk membaca data
4. Mutation: Fungsi-fungsi untuk membuat/mengubah/menghapus data
5. Schema: Menggabungkan Query dan Mutation menjadi satu skema GraphQL

Cara Penggunaan:
--------------
Setelah server berjalan, buka http://localhost:8000/graphql di browser
untuk mengakses GraphQL Playground, tempat Anda bisa mencoba query.
"""

import strawberry  # Library GraphQL untuk Python
from typing import List, Optional  # Untuk tipe data Python yang lebih kaya
from app.supabase_client import supabase  # Koneksi ke database Supabase
from datetime import datetime  # Untuk timestamp

# ======= TIPE DATA GRAPHQL =======
# Mendefinisikan bentuk data yang bisa diakses melalui API
# @strawberry.type menandakan ini adalah tipe data GraphQL

@strawberry.type
class User:
    """Representasi data pengguna."""
    id: int
    username: str
    email: str
    created_at: str
    updated_at: str

@strawberry.type
class Product:
    """Representasi data produk."""
    id: int
    name: str
    description: str
    price: int  # Harga dalam desimal (misalnya Rp 150.000)
    stock: int  # Jumlah stok tersedia
    created_at: str
    updated_at: str

@strawberry.type
class Purchase:
    """Representasi data pembelian."""
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    created_at: str
    updated_at: str

# ======= TIPE INPUT =======
# Digunakan untuk operasi pembuatan/pembaruan data
# @strawberry.input menandakan ini adalah tipe input GraphQL

@strawberry.input
class UserInput:
    """Format data untuk membuat pengguna baru."""
    username: str
    email: str
    password: str

@strawberry.input
class ProductInput:
    """Format data untuk membuat/update produk."""
    name: str
    description: str
    price: int
    stock: int

@strawberry.input
class PurchaseInput:
    """Format data untuk pembelian produk."""
    product_id: int
    quantity: int

# ======= QUERY RESOLVERS =======
# Fungsi-fungsi untuk membaca data dari database
# Query digunakan untuk MEMBACA data, tanpa mengubahnya

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Mendapatkan satu pengguna berdasarkan ID."""
        # Mencari user dengan ID yang diberikan di tabel users
        response = supabase.table("users").select("*").eq("id", id).execute()
        # Jika ditemukan, konversi ke objek User
        if response.data:
            return User(**response.data[0])
        # Jika tidak ditemukan, kembalikan None
        return None
    
    @strawberry.field
    def users(self) -> List[User]:
        """Mendapatkan semua pengguna."""
        # Mengambil semua data dari tabel users
        response = supabase.table("users").select("*").execute()
        # Konversi setiap baris data menjadi objek User
        return [User(**user) for user in response.data]
        
    @strawberry.field
    def product(self, id: int) -> Optional[Product]:
        """Mendapatkan satu produk berdasarkan ID."""
        # Mencari produk dengan ID yang diberikan di tabel products
        response = supabase.table("products").select("*").eq("id", id).execute()
        # Jika ditemukan, konversi ke objek Product
        if response.data:
            return Product(**response.data[0])
        # Jika tidak ditemukan, kembalikan None
        return None
    
    @strawberry.field
    def products(self) -> List[Product]:
        """Mendapatkan semua produk."""
        # Mengambil semua data dari tabel products
        response = supabase.table("products").select("*").execute()
        # Konversi setiap baris data menjadi objek Product
        return [Product(**product) for product in response.data]
    
    @strawberry.field
    def purchase(self, id: int) -> Optional[Purchase]:
        """Mendapatkan satu pembelian berdasarkan ID."""
        # Mencari pembelian dengan ID yang diberikan di tabel purchases
        response = supabase.table("purchases").select("*").eq("id", id).execute()
        # Jika ditemukan, konversi ke objek Purchase
        if response.data:
            return Purchase(**response.data[0])
        # Jika tidak ditemukan, kembalikan None
        return None
    
    @strawberry.field
    def purchases(self) -> List[Purchase]:
        """Mendapatkan semua pembelian."""
        # Mengambil semua data dari tabel purchases
        response = supabase.table("purchases").select("*").execute()
        # Konversi setiap baris data menjadi objek Purchase
        return [Purchase(**purchase) for purchase in response.data]
    
    @strawberry.field
    def user_purchases(self, user_id: int) -> List[Purchase]:
        """Mendapatkan semua pembelian dari satu pengguna."""
        # Mengambil data pembelian berdasarkan user_id
        response = supabase.table("purchases").select("*").eq("user_id", user_id).execute()
        # Konversi setiap baris data menjadi objek Purchase
        return [Purchase(**purchase) for purchase in response.data]

# ======= MUTATION RESOLVERS =======
# Fungsi-fungsi untuk memodifikasi data di database
# Mutation digunakan untuk CREATE, UPDATE, DELETE data

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, product: ProductInput) -> Product:
        """Membuat produk baru di database."""
        # Dapatkan waktu saat ini dalam format ISO
        now = datetime.now().isoformat()
        
        # Siapkan data produk untuk dimasukkan ke database
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert data ke tabel products di Supabase
        response = supabase.table("products").insert(product_data).execute()
        # Kembalikan produk yang berhasil dibuat
        return Product(**response.data[0])
    
    @strawberry.mutation
    def update_product(self, id: int, product: ProductInput) -> Product:
        """Memperbarui produk yang sudah ada di database."""
        # Siapkan data produk yang akan diupdate
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "updated_at": datetime.now().isoformat()  # Update waktu terakhir diubah
        }
        
        # Update data di tabel products berdasarkan ID
        response = supabase.table("products").update(product_data).eq("id", id).execute()
        # Kembalikan produk yang berhasil diupdate
        return Product(**response.data[0])
    
    @strawberry.mutation
    def delete_product(self, id: int) -> bool:
        """Menghapus produk dari database."""
        # Hapus produk dengan ID tertentu dari tabel products
        response = supabase.table("products").delete().eq("id", id).execute()
        # Kembalikan True jika berhasil dihapus, False jika tidak
        return len(response.data) > 0
    
    @strawberry.mutation
    def create_purchase(self, purchase: PurchaseInput, user_id: int) -> Optional[Purchase]:
        """Membuat pembelian baru."""
        # Dapatkan produk yang ingin dibeli
        product_response = supabase.table("products").select("*").eq("id", purchase.product_id).execute()
        
        if not product_response.data:
            return None  # Produk tidak ditemukan
            
        product = product_response.data[0]
        
        # Periksa stok
        if product["stock"] < purchase.quantity:
            return None  # Stok tidak cukup
            
        # Hitung total harga
        total_price = product["price"] * purchase.quantity
        
        # Dapatkan waktu saat ini dalam format ISO
        now = datetime.now().isoformat()
        
        # Siapkan data pembelian
        purchase_data = {
            "user_id": user_id,
            "product_id": purchase.product_id,
            "quantity": purchase.quantity,
            "total_price": total_price,
            "status": "pending",
            "created_at": now,
            "updated_at": now
        }
        
        # Insert data ke tabel purchases
        purchase_response = supabase.table("purchases").insert(purchase_data).execute()
        
        # Update stok produk
        updated_stock = product["stock"] - purchase.quantity
        supabase.table("products").update({"stock": updated_stock, "updated_at": now}).eq("id", purchase.product_id).execute()
        
        # Return data pembelian
        return Purchase(**purchase_response.data[0])
    
    @strawberry.mutation
    def update_purchase_status(self, id: int, status: str) -> Optional[Purchase]:
        """Memperbarui status pembelian."""
        # Periksa apakah status valid
        valid_statuses = ["pending", "completed", "cancelled"]
        if status not in valid_statuses:
            return None
            
        # Update status di database
        response = supabase.table("purchases").update({
            "status": status,
            "updated_at": datetime.now().isoformat()
        }).eq("id", id).execute()
        
        # Kembalikan data pembelian yang diupdate
        if response.data:
            return Purchase(**response.data[0])
        return None

# Buat skema GraphQL yang menggabungkan Query dan Mutation
# Schema ini yang akan digunakan oleh FastAPI untuk membuat endpoint GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation) 