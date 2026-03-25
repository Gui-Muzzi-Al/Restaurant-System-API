from fastapi import FastAPI
from .database import Base, engine
from .routers import products, categories, inventory
from app.routers import orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant API")

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(inventory.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Restaurant API is up and running!"}