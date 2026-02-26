from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Inventory Service")

app.include_router(router, prefix="/inventory")

@router.get("/health")
async def health():
    return {"status": "ok"}