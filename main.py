
from fastapi import FastAPI
from app.routers.order_routers import *
from app.routers.product import *
from app.db.database import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(order_router)
app.include_router(payment_router)
app.include_router(size_router)
app.include_router(stock_router)
app.include_router(router)
app.include_router(product_item_router)
