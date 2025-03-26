from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.product import Product

class ProductController:
    def __init__(self):
        self.products = []

    def get_all(self):
        return self.products
    
    def get_one(self, id: int):
        product = list(filter(lambda p: p.id == id, self.products))

        if len(product) == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product[0]

    def create(self, product: Product):
        print(product)
        self.products.append(product)
        return JSONResponse(content={ "message": "Product created" })
