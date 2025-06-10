from pydantic import BaseModel, ConfigDict,model_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: str
    image_url: Optional[str]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update.")
        return values

class ProductResponse(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

