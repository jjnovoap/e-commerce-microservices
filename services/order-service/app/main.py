from fastapi import APIRouter
from app.routers import router
from app.database import Base, engine

app = FastAPI(title="Order Service")

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/orders")