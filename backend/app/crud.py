from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_purchase(db: Session, purchase: schemas.PurchaseCreate, user_id: int):
    # Get the product
    product = get_product(db, purchase.product_id)
    if not product or product.stock < purchase.quantity:
        return None
    
    # Calculate total price
    total_price = product.price * purchase.quantity
    
    # Create purchase record
    db_purchase = models.Purchase(
        user_id=user_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        total_price=total_price,
        status="pending"
    )
    
    # Update product stock
    product.stock -= purchase.quantity
    
    # Commit changes
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_user_purchases(db: Session, user_id: int):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

def update_purchase_status(db: Session, purchase_id: int, status: str):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase:
        db_purchase.status = status
        db.commit()
        db.refresh(db_purchase)
    return db_purchase