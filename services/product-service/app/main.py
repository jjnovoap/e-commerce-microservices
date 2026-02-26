from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.routers import products

app = FastAPI(title="Product Service")

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)


# ===============================
# MANEJO GLOBAL DE VALIDACIONES
# ===============================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors()
        }
    )


# ===============================
# MANEJO GLOBAL DE ERRORES SQL
# ===============================
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error"
        }
    )


# ===============================
# ROUTERS
# ===============================
app.include_router(products.router, prefix="/products", tags=["Products"])


# ===============================
# HEALTH CHECK
# ===============================
@app.get("/health")
def health():
    return {"status": "ok"}