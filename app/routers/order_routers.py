from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order_schemas import (
    OrderCreate, OrderRead, PaymentCreate, PaymentRead, SizeCreate,
    SizeRead, SizeStockCreate, SizeStockRead, ColorStockCreate,
    ColorStockRead, ProductCreate, ProductRead, ColorCreate, ColorRead)
from app.crud.order_crud import (
    create_order, get_order, create_payment, get_payment, create_size,
    get_size, create_size_stock, create_color_stock, create_product,
    create_color, get_user_orders, get_user_payments)

# routes/order_routes.py

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get("/orders/{user_id}", response_model=list[OrderRead])
def read_user_orders(user_id: int, db: Session = Depends(get_db)):
    return get_user_orders(db, user_id)


@order_router.post("/", response_model=OrderRead)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)


@order_router.get("/{order_id}", response_model=OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# routes/payment_routes.py

payment_router = APIRouter(prefix="/payments", tags=["Payments"])

@payment_router.post("/", response_model=PaymentRead)
def create_new_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(db, payment)

@payment_router.get("/{payment_id}", response_model=PaymentRead)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@payment_router.get("/payments/{user_id}", response_model=list[PaymentRead])
def read_user_payments(user_id: int, db: Session = Depends(get_db)):
    return get_user_payments(db, user_id)

# routes/size_routes.py

size_router = APIRouter(prefix="/sizes", tags=["Sizes"])

@size_router.post("/", response_model=SizeRead)
def create_new_size(size: SizeCreate, db: Session = Depends(get_db)):
    return create_size(db, size)

@size_router.get("/{size_id}", response_model=SizeRead)
def read_size(size_id: int, db: Session = Depends(get_db)):
    size = get_size(db, size_id)
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")
    return size

# routes/stock_routes.py

stock_router = APIRouter(prefix="/stocks", tags=["Stocks"])

@stock_router.post("/size", response_model=SizeStockRead)
def create_new_size_stock(size_stock: SizeStockCreate, db: Session = Depends(get_db)):
    return create_size_stock(db, size_stock)

@stock_router.post("/color", response_model=ColorStockRead)
def create_new_color_stock(color_stock: ColorStockCreate, db: Session = Depends(get_db)):
    return create_color_stock(db, color_stock)

# routes/product_routes.py

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.post("/", response_model=ProductRead)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@product_router.post("/colors", response_model=ColorRead)
def create_new_color(color: ColorCreate, db: Session = Depends(get_db)):
    return create_color(db, color)
