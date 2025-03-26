from fastapi import APIRouter
from app.controllers.products import ProductController
from app.models.product import Product

router = APIRouter(prefix="/api/products")
controller = ProductController()

@router.get("")
def get_all():
    return controller.get_all()

@router.get("/{id}")
def get_one(id: int):
    return controller.get_one(id)

@router.post("")
def create(product: Product):
    return controller.create(product)