from pydantic import BaseModel

class InventoryReserve(BaseModel):
    product_id: int
    quantity: int

class InventoryResponse(BaseModel):
    product_id: int
    stock: int

    class Config:
        orm_mode = True