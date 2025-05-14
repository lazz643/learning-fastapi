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

# Optional database session dependency - hanya digunakan oleh endpoint REST
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint untuk health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running. Use /graphql for GraphQL API"}

# --- Endpoint REST berikut ini opsional dan mungkin tidak berfungsi tanpa MySQL ---

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return crud.create_user(db, user)
    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user_db = crud.authenticate_user(db, user.username, user.password)
        if not user_db:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = auth.create_access_token(data={"sub": user_db.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_product(db, product)
    except Exception as e:
        logger.error(f"Error in create_product endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error, try using GraphQL API")