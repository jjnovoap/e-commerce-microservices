from fastapi import FastAPI
import httpx
import os
#from app.routes import router
#app = FastAPI(title="Product Service")
#app.include_router(router)

app = FastAPI()

products_db = {
    1: {"id": 1, "name": "Laptop", "price": 1200},
    2: {"id": 2, "name": "Mouse", "price": 25}
}

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

@app.get("/products/{product_id}")
async def get_product(product_id: int):

    product = products_db.get(product_id)

    if not product:
        return {"error": "Product not found"}

    async with httpx.AsyncClient() as client:
        inventory_response = await client.get(f"{INVENTORY_SERVICE_URL}/inventory/{product_id}")
        
        inventory_data = inventory_response.json()

    return {"product": product, "inventory": inventory_data}

@app.get("/health")
async def health():
    return {"status": "ok"}