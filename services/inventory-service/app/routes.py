from fastapi import APIRouter, HTTPException
from app.models import Inventory

router = APIRouter()

inventory_db = {
    1: {"product_id": 1, "stock": 10},
    2: {"product_id": 2, "stock": 5},
}

@router.get("/products/health")
async def health():
    return {"status": "ok"}

@router.get("/{product_id}", response_model=Inventory)
def get_inventory(product_id: int):
    inventory = inventory_db.get(product_id)

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return inventory