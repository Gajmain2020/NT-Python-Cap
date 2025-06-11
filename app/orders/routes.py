from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.auth.routes import get_db
from app.utils.response import create_response
from app.orders.models import Order, OrderItem
from app.products.models import Product
from app.cart.models import Cart
from app.orders.schemas import OrderResponse, OrderDetailResponse, OrderItemResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/order_health_check")
def order_health_check():
    return create_response(data={"message": "Order health check is done."})

@router.post("/checkout")
def checkout(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart_items = db.query(Cart).filter_by(user_id=user["id"]).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart_items:
        if item.quantity > item.product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{item.product.name}'"
            )

    order = Order(user_id=user["id"], total=0)
    db.add(order)
    db.commit()

    total = 0
    for item in cart_items:
        product = item.product
        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        ))
        total += subtotal

    order.total = total
    db.query(Cart).filter_by(user_id=user["id"]).delete()
    db.commit()

    return create_response(data={"message": "Order placed successfully", "order_id": order.id})

@router.get("/", response_model=list[OrderResponse])
def view_order_history(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    orders = db.query(Order).filter_by(user_id=user["id"]).order_by(Order.created_at.desc()).all()
    return orders

@router.get("/{order_id}", response_model=OrderDetailResponse)
def view_order_detail(order_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    order = db.query(Order).filter_by(id=order_id, user_id=user["id"]).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = []
    for item in order.items:
        items.append(OrderItemResponse(
            product_id=item.product_id,
            product_name=item.product.name,
            quantity=item.quantity,
            subtotal=item.quantity * item.price
        ))

    return OrderDetailResponse(
        id=order.id,
        created_at=order.created_at,
        total=order.total,
        status=order.status,
        items=items
    )
