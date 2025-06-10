from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.routes import get_db
from app.products.schemas import ProductResponse
from app.utils.response import create_response
from sqlalchemy.orm import Session
from app.products.models import Product
from fastapi.exceptions import HTTPException

router = APIRouter(tags=["Public Products"])

@router.get('/public_product_health_check')
def health_check():
    return create_response(data={"message": "Health Check is done."})

@router.get("/products", response_model=list[ProductResponse])
def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query("id", enum=["id", "price", "name"]),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    query = query.order_by(getattr(Product, sort_by))
    products = query.offset((page - 1) * page_size).limit(page_size).all()
    return products

@router.get("/products/search", response_model=list[ProductResponse])
def search_products(keyword: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.ilike(f"%{keyword}%")).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
