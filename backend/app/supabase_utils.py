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

def authenticate_supabase_user(username: str, password: str):
    """Authenticate a user against Supabase data"""
    user = get_supabase_user_by_username(username)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return None
    return user

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