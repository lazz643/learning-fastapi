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

# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation) 