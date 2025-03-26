from fastapi import FastAPI
from app.routes import product

app = FastAPI(
    title="API",
    description="backend-interview-python",
    version="1.0.0",
    servers=[
        {"url": "http://localhost:8000", "description": "Localhost"}
    ],
)

app.include_router(product.router)
