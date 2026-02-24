from fastapi import APIRouter, HTTPException
from app.models import ProductCreate, Product, ProductWithInventory
import httpx
import os

router = APIRouter()

products_db = {
    1: {"id": 1, "name": "Laptop", "price": 1200},
    2: {"id": 2, "name": "Mouse", "price": 25},
}

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/{product_id}", response_model=ProductWithInventory)
async def get_product(product_id: int):

    product = products_db.get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not INVENTORY_SERVICE_URL:
        raise HTTPException(status_code=500, detail="Inventory URL not configured")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            inventory_response = await client.get(
                f"{INVENTORY_SERVICE_URL}/inventory/{product_id}"
            )

            inventory_response.raise_for_status()
            inventory_data = inventory_response.json()

    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Inventory service unavailable")

    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Inventory service error")

    return {
        "product": product,
        "inventory": inventory_data
    }


@router.post("/")
def create_product(product: ProductCreate):
    new_id = max(products_db.keys()) + 1
    new_product = {"id": new_id, **product.dict()}
    products_db[new_id] = new_product
    return new_product


@router.get("/")
def list_products():
    return list(products_db.values())