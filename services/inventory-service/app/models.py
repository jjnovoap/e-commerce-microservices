from pydantic import BaseModel

class Inventory(BaseModel):
    product_id: int
    stock: int