from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.cart.models import Cart
from app.products.models import Product
from app.cart.schemas import AddToCart
from app.utils.response import create_response
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/cart_health_check')
def cart_health_check():
    return create_response(data={"message": "Cart Health Check is done."})

# Add to Cart
@router.post("/")
def add_to_cart(data: AddToCart, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    # Fetch product to check stock
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch existing cart item if any
    existing = db.query(Cart).filter_by(user_id=user["id"], product_id=data.product_id).first()

    # Calculate total quantity in cart after this addition
    new_quantity = data.quantity
    if existing:
        new_quantity += existing.quantity

    # Validate stock availability
    if new_quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock - (existing.quantity if existing else 0)} items left in stock."
        )

    # Update or add cart item
    if existing:
        existing.quantity = new_quantity
    else:
        new_item = Cart(user_id=user["id"], product_id=data.product_id, quantity=data.quantity)
        db.add(new_item)

    db.commit()
    return create_response(data={"detail": "Item added to cart"})
