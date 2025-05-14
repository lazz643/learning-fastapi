from pydantic import BaseModel

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