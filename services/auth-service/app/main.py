from fastapi import FastAPI
from .database import Base, engine
from .router import router

app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(router)