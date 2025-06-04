
from fastapi import FastAPI
from app.routers.order_routers import (
    order_router, payment_router, size_router, stock_router, product_router)
from app.routers.product import (
    router, product_item_router, product_image_router, product_price_router,
    color_router)
from app.routers.acount_router import(
    country_router
)
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(order_router)
app.include_router(payment_router)
app.include_router(size_router)
app.include_router(stock_router)
app.include_router(product_router)
app.include_router(router)
app.include_router(product_item_router)
app.include_router(product_image_router)
app.include_router(product_price_router)
app.include_router(color_router)
app.include_router(country_router)
