from fastapi import APIRouter
from app.models import Product

router = APIRouter()

products = []


@router.post("/products")
def create_product(product: Product):
    products.append(product)
    return product


@router.get("/products")
def list_products():
    return products
