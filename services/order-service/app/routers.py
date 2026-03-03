from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order
from app.schemas import OrderCreate
from app.services import validate_product, reserve_stock
from .security import verify_token

router = APIRouter()

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
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    # 1️⃣ Validar producto
    if not await validate_product(order.product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    # 2️⃣ Reservar stock (descuento real)
    if not await reserve_stock(order.product_id, order.quantity):
        new_order = Order(
            product_id=order.product_id,
            quantity=order.quantity,
            status="REJECTED_NO_STOCK"
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    # 3️⃣ Crear orden
    new_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        status="CREATED"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order