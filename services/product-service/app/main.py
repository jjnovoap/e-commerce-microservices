from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Product Service")

app.include_router(router, prefix="/products")