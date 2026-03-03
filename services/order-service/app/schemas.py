from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True