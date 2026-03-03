from sqlalchemy.orm import Session
from app.models import Inventory
from fastapi import HTTPException

def reserve_stock_logic(db: Session, product_id: int, quantity: int):

    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == product_id)
        .with_for_update()
        .first()
    )

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    if inventory.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    inventory.stock -= quantity
    db.commit()

    return inventory