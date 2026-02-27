from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from httpx
import os

from app.database import SessionLocal
from app,models import Order
from app.schemas import OrderCreate

router = APIRouter()

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/", status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    # 1️⃣ Validar producto
    product_response = httpx.get(
        f"{PRODUCT_SERVICE_URL}/{order.product_id}"
    )
    if product_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2️⃣ Validar inventario
    inventory_response = httpx.get(
        f"{INVENTORY_SERVICE_URL}/{order.product_id}"
    )
    if inventory_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory_data = inventory_response.json()

    if inventory_data["stock"] < order.quantity:
        new_order = Order(
            product_id=order.product_id,
            quantity=order.quantity,
            status="REJECTED_NO_STOCK",
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    # 3️⃣ Crear orden
    new_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        status="CREATED",
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order