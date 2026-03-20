from pydantic import BaseModel

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