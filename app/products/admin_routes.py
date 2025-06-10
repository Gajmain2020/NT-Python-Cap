from fastapi import APIRouter,Depends,HTTPException 
from app.utils.response import create_response
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.products.schemas import ProductCreate, ProductResponse
from app.products.models import Product
from app.auth.dependencies import require_admin
router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/admin_health_check')
async def admin_health_check():
    return create_response(data={"message": "Admin Health Check is done."})

@router.post("/products", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    # print("product data",product_data)
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        image_url=product_data.image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    response_model = ProductResponse.model_validate(product, from_attributes=True)
    return create_response(data=response_model.model_dump())

@router.get("/products", response_model=list[ProductResponse])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


