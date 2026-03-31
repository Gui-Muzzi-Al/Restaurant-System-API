from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category: CategoryResponse | None = None

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    name: str

    class Config:
        orm_mode = True

class InventoryMovementBase(BaseModel):
    product_id: int
    quantity: int
    movement_type: str
    description: str | None = None

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovementResponse(InventoryMovementBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    status: Optional[str] = None

class OrderCreate(OrderBase):
    pass 

class OrderItemCreate(OrderItemBase):
    product_id: int
    quanti: int


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_moment: float

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    status: str
    total: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []

    class Config:
        orm_mode = True


class OrderItemUpdate(BaseModel):
    quantity: int