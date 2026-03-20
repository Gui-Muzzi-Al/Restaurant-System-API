from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post('/', response_model=schemas.InventoryMovementResponse)
def create_movement(movement: schemas.InventoryMovementCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == movement.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=('Product not found'))
    
    if movement.quantity < 0 and product.stock + movement.quantity < 0: # type: ignore[operator]
        raise HTTPException(status_code=400, detail="Insufficient stock")

    new_movement = models.InventoryMovement(**movement.model_dump())
    db.add(new_movement)

    product.stock = product.stock + movement.quantity # type: ignore[operator]

    db.commit()
    db.refresh(new_movement)
    return new_movement

@router.get("/", response_model=list[schemas.InventoryMovementResponse])
def list_movement(db: Session = Depends(get_db)):
    return db.query(models.InventoryMovement).all()