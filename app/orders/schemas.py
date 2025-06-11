from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    subtotal: float

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    total: float
    status: str

class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse]
