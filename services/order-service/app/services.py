import httpx
import os

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

async def validate_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}"
        )
        return response.status_code == 200

async def reserve_stock(product_id: int, quantity: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{INVENTORY_SERVICE_URL}/inventory/reserve",
            json={"product_id": product_id, "quantity": quantity}
        )
        return response.status_code == 200