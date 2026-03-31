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


@router.post("/orders/{order_id}/items", response_model=schemas.OrderResponse)
def add_item_to_order_v2(order_id: int, item_data: schemas.OrderItemCreate, db: Session = Depends(get_db)):

    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "open":
        raise HTTPException(status_code=400, detail="Cannot add items to a closed order")

    product: models.Product | None = (
        db.query(models.Product)
        .filter(models.Product.id == item_data.product_id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    new_item = models.OrderItem(
        order_id=order_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        price_at_moment=product.price
    )

    db.add(new_item)

    order.total += product.price * item_data.quantity

    db.commit()
    db.refresh(order)

    return order

@router.put("/orders/{order_id}/items/{item_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, item_id: int, item_data: schemas.OrderItemUpdate, db: Session = Depends(get_db)):

    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "open":
        raise HTTPException(status_code=400, detail="Cannot update items in a closed order")
    
    item = (db.query(models.OrderItem).filter(models.OrderItem.id == item_id, models.OrderItem.order_id == order_id).first())

    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    quantity_difference = item_data.quantity - item.quantity

    if quantity_difference > 0 and product.stock < quantity_difference:
        raise HTTPException(status_code=400, detail="Not enough stock for update")
    
    item.quantity = item_data.quantity

    order.total = sum(
        i.quantity * i.price_at_moment for i in order.items
    )

    db.commit()
    db.refresh(order)

@router.delete("/orders/{order_id}/items/{item_id}", response_model=schemas.OrderResponse)
def remove_order_item(order_id: int, item_id: int, db: Session = Depends(get_db)):

    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "open":
        raise HTTPException(status_code=400, detail="Cannot remove items from a closed order")

    item = (
        db.query(models.OrderItem)
        .filter(models.OrderItem.id == item_id, models.OrderItem.order_id == order_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    db.delete(item)
    
    order.total = sum(
        i.quantity * i.price_at_moment
        for i in order.items
        if i.id != item_id
    )

    db.commit()
    db.refresh(order)

    return order
