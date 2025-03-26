from pydantic import BaseModel

class Product(BaseModel):
    id: int
    category: str
    name: str
    price: float
    stock: int
