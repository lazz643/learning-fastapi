# Dokumentasi Lengkap Integrasi FastAPI, Supabase, dan GraphQL

## Daftar Isi
1. [Struktur Proyek](#struktur-proyek)
2. [Setup Awal](#setup-awal)
3. [Supabase](#supabase)
4. [GraphQL](#graphql)
5. [Autentikasi](#autentikasi)
6. [API Endpoints](#api-endpoints)
7. [Contoh Penggunaan](#contoh-penggunaan)
8. [Fitur Pembelian](#fitur-pembelian)
9. [Troubleshooting](#troubleshooting)

## Struktur Proyek

Proyek ini mengintegrasikan FastAPI dengan Supabase sebagai database dan GraphQL untuk API.

```
learning-fastapi/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point aplikasi
│   │   ├── database.py          # Konfigurasi database
│   │   ├── models.py            # Model SQLAlchemy
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # Autentikasi JWT
│   │   ├── crud.py              # CRUD operations (SQLAlchemy)
│   │   ├── supabase_client.py   # Konfigurasi Supabase
│   │   ├── supabase_utils.py    # Fungsi-fungsi helper Supabase
│   │   ├── graphql_schema.py    # Schema GraphQL
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── graphql_routes.py # Router GraphQL
│   ├── test_supabase.py         # Script test koneksi Supabase
│   └── requirements.txt         # Dependensi proyek
```

## Setup Awal

### 1. Instalasi Dependensi

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (macOS/Linux)
source venv/bin/activate

# Install dependensi
pip install -r backend/requirements.txt
```

### 2. File `.env`

Buat file `.env` di folder `backend/` dengan isi:

```
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# JWT Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Supabase

### Konfigurasi Supabase

File: `backend/app/supabase_client.py`
```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### Fungsi Utilitas Supabase

File: `backend/app/supabase_utils.py`
```python
from app.supabase_client import supabase
from passlib.context import CryptContext
from app import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User operations
def create_supabase_user(user: schemas.UserCreate):
    """Create a new user in Supabase"""
    hashed_password = pwd_context.hash(user.password)
    
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    response = supabase.table("users").insert(user_data).execute()
    return response.data[0] if response.data else None

def get_supabase_user_by_username(username: str):
    """Get a user by username from Supabase"""
    response = supabase.table("users").select("*").eq("username", username).execute()
    return response.data[0] if response.data else None

# Product operations
def create_supabase_product(product: schemas.ProductCreate):
    """Create a new product in Supabase"""
    product_data = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }
    
    response = supabase.table("products").insert(product_data).execute()
    return response.data[0] if response.data else None

def get_supabase_product(product_id: int):
    """Get a product by ID from Supabase"""
    response = supabase.table("products").select("*").eq("id", product_id).execute()
    return response.data[0] if response.data else None

def get_all_supabase_products():
    """Get all products from Supabase"""
    response = supabase.table("products").select("*").execute()
    return response.data

def update_supabase_product(product_id: int, product: schemas.ProductCreate):
    """Update a product in Supabase"""
    product_data = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }
    
    response = supabase.table("products").update(product_data).eq("id", product_id).execute()
    return response.data[0] if response.data else None

def delete_supabase_product(product_id: int):
    """Delete a product from Supabase"""
    response = supabase.table("products").delete().eq("id", product_id).execute()
    return len(response.data) > 0
```

### Schema Pydantic

File: `backend/app/schemas.py`
```python
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int

    class Config:
        from_attributes = True

class PurchaseCreate(BaseModel):
    product_id: int
    quantity: int
    
class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    
    class Config:
        from_attributes = True
```

### Model SQLAlchemy

File: `backend/app/models.py`
```python
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(Integer)
    stock = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Integer)
    status = Column(String(50), default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
```

## GraphQL

### Schema GraphQL

File: `backend/app/graphql_schema.py`
```python
import strawberry
from typing import List, Optional
from app.supabase_client import supabase
from datetime import datetime

# GraphQL types
@strawberry.type
class User:
    id: int
    username: str
    email: str
    created_at: str
    updated_at: str

@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: int
    stock: int
    created_at: str
    updated_at: str

@strawberry.type
class Purchase:
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    created_at: str
    updated_at: str

# Input types
@strawberry.input
class UserInput:
    username: str
    email: str
    password: str

@strawberry.input
class ProductInput:
    name: str
    description: str
    price: int
    stock: int

@strawberry.input
class PurchaseInput:
    product_id: int
    quantity: int

# Query resolvers
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        response = supabase.table("users").select("*").eq("id", id).execute()
        if response.data:
            return User(**response.data[0])
        return None
    
    @strawberry.field
    def users(self) -> List[User]:
        response = supabase.table("users").select("*").execute()
        return [User(**user) for user in response.data]
        
    @strawberry.field
    def product(self, id: int) -> Optional[Product]:
        response = supabase.table("products").select("*").eq("id", id).execute()
        if response.data:
            return Product(**response.data[0])
        return None
    
    @strawberry.field
    def products(self) -> List[Product]:
        response = supabase.table("products").select("*").execute()
        return [Product(**product) for product in response.data]

    @strawberry.field
    def purchase(self, id: int) -> Optional[Purchase]:
        response = supabase.table("purchases").select("*").eq("id", id).execute()
        if response.data:
            return Purchase(**response.data[0])
        return None
    
    @strawberry.field
    def purchases(self) -> List[Purchase]:
        response = supabase.table("purchases").select("*").execute()
        return [Purchase(**purchase) for purchase in response.data]
    
    @strawberry.field
    def user_purchases(self, user_id: int) -> List[Purchase]:
        response = supabase.table("purchases").select("*").eq("user_id", user_id).execute()
        return [Purchase(**purchase) for purchase in response.data]

# Mutation resolvers
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, product: ProductInput) -> Product:
        now = datetime.now().isoformat()
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "created_at": now,
            "updated_at": now
        }
        
        response = supabase.table("products").insert(product_data).execute()
        return Product(**response.data[0])
    
    @strawberry.mutation
    def update_product(self, id: int, product: ProductInput) -> Product:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.table("products").update(product_data).eq("id", id).execute()
        return Product(**response.data[0])
    
    @strawberry.mutation
    def delete_product(self, id: int) -> bool:
        response = supabase.table("products").delete().eq("id", id).execute()
        return len(response.data) > 0

    @strawberry.mutation
    def create_purchase(self, purchase: PurchaseInput, user_id: int) -> Optional[Purchase]:
        # Get the product
        product_response = supabase.table("products").select("*").eq("id", purchase.product_id).execute()
        
        if not product_response.data:
            return None  # Product not found
            
        product = product_response.data[0]
        
        # Check stock
        if product["stock"] < purchase.quantity:
            return None  # Insufficient stock
            
        # Calculate total price
        total_price = product["price"] * purchase.quantity
        
        # Current time in ISO format
        now = datetime.now().isoformat()
        
        # Purchase data
        purchase_data = {
            "user_id": user_id,
            "product_id": purchase.product_id,
            "quantity": purchase.quantity,
            "total_price": total_price,
            "status": "pending",
            "created_at": now,
            "updated_at": now
        }
        
        # Insert purchase record
        purchase_response = supabase.table("purchases").insert(purchase_data).execute()
        
        # Update product stock
        updated_stock = product["stock"] - purchase.quantity
        supabase.table("products").update({"stock": updated_stock, "updated_at": now}).eq("id", purchase.product_id).execute()
        
        # Return purchase data
        return Purchase(**purchase_response.data[0])
    
    @strawberry.mutation
    def update_purchase_status(self, id: int, status: str) -> Optional[Purchase]:
        # Valid status values
        valid_statuses = ["pending", "completed", "cancelled"]
        if status not in valid_statuses:
            return None
            
        # Update purchase status
        response = supabase.table("purchases").update({
            "status": status,
            "updated_at": datetime.now().isoformat()
        }).eq("id", id).execute()
        
        # Return updated purchase
        if response.data:
            return Purchase(**response.data[0])
        return None

# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### GraphQL Routes

File: `backend/app/endpoints/graphql_routes.py`
```python
from fastapi import Depends, HTTPException, status
from strawberry.fastapi import GraphQLRouter
from app.graphql_schema import schema
from app.auth import get_current_user

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Create a protected GraphQL router that requires authentication
async def get_context(request):
    """Get context for GraphQL operations requiring authentication"""
    try:
        # Get token from Authorization header
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            user = await get_current_user(token)
            return {"user": user}
        raise HTTPException(status_code=401)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

protected_graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)
```

## Autentikasi

### JWT Autentikasi 

File: `backend/app/auth.py`
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # In a full implementation, you would fetch the user from the database here
    # For now, we just return the username
    return {"username": username}
```

## Entry Point Aplikasi (main.py)

File: `backend/app/main.py`
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud, auth
from app.endpoints.graphql_routes import graphql_app, protected_graphql_app
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Jika ada model SQLAlchemy yang perlu dibuat
    models.Base.metadata.create_all(bind=engine)
    logger.info("SQLAlchemy models created")
except Exception as e:
    logger.warning(f"Could not create SQLAlchemy models: {e}")
    logger.info("Continuing without SQLAlchemy models - using Supabase only")

app = FastAPI()

# Add GraphQL endpoints - Ini adalah fokus utama aplikasi
app.include_router(graphql_app, prefix="/graphql")
app.include_router(protected_graphql_app, prefix="/graphql/protected")

# Root endpoint untuk health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running. Use /graphql for GraphQL API"}
```

## API Endpoints

### GraphQL Endpoints

- **Public GraphQL**: `http://localhost:8000/graphql`
  - Tidak memerlukan autentikasi
  - Dapat digunakan untuk query/mutation dasar

- **Protected GraphQL**: `http://localhost:8000/graphql/protected`
  - Memerlukan token JWT di header Authorization
  - Untuk operasi yang memerlukan autentikasi

## Contoh Penggunaan

### 1. Menjalankan Aplikasi

```bash
cd backend
uvicorn app.main:app --reload
```

### 2. Test Koneksi Supabase

```bash
cd backend
python test_supabase.py
```

### 3. Menggunakan GraphQL

#### Query Products

```graphql
query {
  products {
    id
    name
    description
    price
    stock
    created_at
    updated_at
  }
}
```

#### Query Single Product

```graphql
query {
  product(id: 1) {
    id
    name
    description
    price
    stock
  }
}
```

#### Create Product

```graphql
mutation {
  createProduct(
    product: {
      name: "Laptop Gaming",
      description: "Laptop gaming high-end",
      price: 15000000,
      stock: 10
    }
  ) {
    id
    name
    description
    price
    stock
  }
}
```

#### Update Product

```graphql
mutation {
  updateProduct(
    id: 1,
    product: {
      name: "Updated Product",
      description: "New description",
      price: 12000000,
      stock: 5
    }
  ) {
    id
    name
    description
    price
    stock
  }
}
```

#### Delete Product

```graphql
mutation {
  deleteProduct(id: 1)
}
```

## Fitur Pembelian

### 1. Membuat Tabel Purchases di Supabase

1. Login ke [Supabase Dashboard](https://app.supabase.com)
2. Pilih project Anda
3. Klik "Table Editor" di sidebar
4. Klik "Create a new table"
5. Buat tabel "purchases" dengan kolom:
   - id (type: int8, primary, identity)
   - user_id (type: int8, foreign key ke users.id)
   - product_id (type: int8, foreign key ke products.id)
   - quantity (type: int4)
   - total_price (type: int4)
   - status (type: text, default: 'pending')
   - created_at (type: timestamptz, default: now())
   - updated_at (type: timestamptz, default: now())
6. Klik "Save"

#### Query SQL untuk Membuat Tabel Purchases

Anda juga bisa menggunakan SQL Editor di Supabase untuk membuat tabel dengan query berikut:

```sql
-- Membuat tabel purchases
CREATE TABLE purchases (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id),
  product_id BIGINT REFERENCES products(id),
  quantity INTEGER NOT NULL,
  total_price INTEGER NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Membuat index untuk mempercepat query
CREATE INDEX idx_purchases_user_id ON purchases(user_id);
CREATE INDEX idx_purchases_product_id ON purchases(product_id);
CREATE INDEX idx_purchases_status ON purchases(status);
```

#### Query SQL untuk Operasi Umum

```sql
-- Melihat semua pembelian
SELECT * FROM purchases;

-- Melihat pembelian untuk user tertentu
SELECT p.*, pr.name as product_name
FROM purchases p
JOIN products pr ON p.product_id = pr.id
WHERE p.user_id = 1;

-- Melihat detail pembelian dengan informasi produk
SELECT 
  p.id, 
  p.quantity, 
  p.total_price, 
  p.status, 
  p.created_at,
  pr.name as product_name, 
  pr.price as product_price,
  u.username as buyer
FROM purchases p
JOIN products pr ON p.product_id = pr.id
JOIN users u ON p.user_id = u.id
WHERE p.id = 1;

-- Mengubah status pembelian
UPDATE purchases
SET status = 'completed', updated_at = now()
WHERE id = 1;

-- Menambahkan kolom catatan untuk pembelian (jika diperlukan)
ALTER TABLE purchases
ADD COLUMN notes TEXT;
```

### 2. Contoh GraphQL untuk Pembelian

#### Membuat Pembelian Baru

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
    created_at
  }
}
```

#### Melihat Semua Pembelian

```graphql
query {
  purchases {
    id
    user_id
    product_id
    quantity
    total_price
    status
    created_at
  }
}
```

#### Melihat Pembelian Pengguna Tertentu

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

#### Mengubah Status Pembelian

```graphql
mutation {
  updatePurchaseStatus(
    id: 1,
    status: "completed"
  ) {
    id
    status
    updated_at
  }
}
```

### 3. REST API untuk Pembelian

Endpoint | Method | Fungsi
---------|--------|-------
`/purchases` | POST | Membuat pembelian baru (memerlukan autentikasi)
`/purchases/me` | GET | Mendapatkan daftar pembelian pengguna yang login (memerlukan autentikasi)

#### Contoh Request untuk Membuat Pembelian

```bash
curl -X POST "http://localhost:8000/purchases" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"product_id": 1, "quantity": 2}'
```

## Troubleshooting

### 1. Supabase Connection Issues

- Periksa SUPABASE_URL dan SUPABASE_KEY di file .env
- Pastikan menggunakan anon key, bukan service_role key
- Periksa apakah tabel sudah dibuat di Supabase

### 2. GraphQL Errors

- Pastikan field yang diminta ada di tabel Supabase
- Periksa syntax GraphQL (kurung, koma, tanda kutip)
- Untuk endpoint protected, pastikan header Authorization sudah benar

### 3. Database Error

- Jika menggunakan fitur SQLAlchemy, periksa .env untuk konfigurasi database
- Database.py telah dimodifikasi untuk tidak memerlukan MySQL dan fokus pada Supabase

### 4. Masalah Pembelian

- **Invalid product or insufficient stock**: Pastikan produk ada dan memiliki stok cukup
- **Auth error pada endpoint pembelian**: Pastikan token JWT valid dan disertakan di header
- **Status tidak berubah**: Pastikan menggunakan nilai status yang valid (pending, completed, cancelled)

---

# Panduan Langkah-demi-Langkah

## Membuat Tabel di Supabase

1. Login ke [Supabase Dashboard](https://app.supabase.com)
2. Pilih project Anda
3. Klik "Table Editor" di sidebar
4. Klik "Create a new table"
5. Buat tabel "products" dengan kolom:
   - id (type: int8, primary, identity)
   - name (type: text)
   - description (type: text)
   - price (type: int4)
   - stock (type: int4)
   - created_at (type: timestamptz, default: now())
   - updated_at (type: timestamptz, default: now())
6. Klik "Save"

## Menjalankan Aplikasi

1. Pastikan file `.env` berisi SUPABASE_URL dan SUPABASE_KEY yang benar
2. Aktifkan virtual environment
3. Jalankan: `cd backend && uvicorn app.main:app --reload`
4. Buka browser dan kunjungi http://localhost:8000/graphql

## Mencoba Query GraphQL

1. Di GraphQL Playground, ketik query untuk mendapatkan semua produk
2. Klik tombol Play (▶️) di tengah
3. Hasil akan muncul di panel kanan

## Menggunakan Autentikasi (Opsional)

1. Register user melalui endpoint REST: `/register`
2. Login untuk mendapatkan token: `/login`
3. Gunakan token di header Authorization untuk mengakses `/graphql/protected` 