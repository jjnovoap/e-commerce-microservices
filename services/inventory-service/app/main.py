from fastapi import FastAPI

app = FastAPI()

inventory_db = {1: {"product_id": 1, "stock": 10}, 2: {"product_id": 2, "stock": 5}}


@app.get("/inventory/{product_id}")
def get_inventory(product_id: int):
    return inventory_db.get(product_id, {"error": "Not found"})


@app.get("/health")
async def health():
    return {"status": "ok"}
