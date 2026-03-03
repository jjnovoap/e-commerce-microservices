from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Inventory
from app.schemas import InventoryReserve

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/{product_id}")
def get_inventory(product_id: int, db: Session = Depends(get_db)):

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return inventory


@router.post("/reserve")
def reserve_stock(data: InventoryReserve, db: Session = Depends(get_db)):

    inventory = db.query(Inventory).filter(
        Inventory.product_id == data.product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    if inventory.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    inventory.stock -= data.quantity

    db.commit()
    db.refresh(inventory)

    return {
        "message": "Stock reserved",
        "remaining_stock": inventory.stock
    }