from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

class Inventory(BaseModel):
    product_id: int
    stock: int

class ProductWithInventory(BaseModel):
    product: Product
    inventory: Inventory