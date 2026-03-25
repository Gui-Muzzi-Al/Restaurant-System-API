from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order  = models.Order()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.post("{order_id}/items", response_model=schemas.OrderResponse)
def add_item_to_order(order_id: int, item_data: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "open": # type: ignore
        raise HTTPException(status_code=400, detail="Cannot add items to a closed order")
    
    product = db.query(models.Product).filter(models.Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_item = models.OrderItem(
        order_id=order_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        price_at_moment=product.price
    )

    db.add(new_item)

    order.total = order.total + (product.price * item_data.quantity) # type: ignore

    db.commit()
    db.refresh(order)

    return order

