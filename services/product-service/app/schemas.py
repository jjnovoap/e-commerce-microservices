from pydantic import BaseModel, Field

# ==========================
# ESQUEMA PARA CREAR PRODUCTO
# ==========================
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)

# ==========================
# ESQUEMA DE RESPUESTA
# ==========================
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True