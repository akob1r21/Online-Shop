from sqlalchemy.orm import Session
from app.models.models import (
    Order, OrderItem, Payment, Size, SizeStock, ColorStock)
from app.schemas.order_schemas import (
    OrderCreate, ProductCreate, ColorCreate, PaymentCreate, SizeStockCreate,
    ColorStockCreate, SizeCreate)
from app.models.product_model import Product, Color

# crud/order_crud.py


def create_order(db: Session, order_data: OrderCreate) -> Order:
    order = Order(
        user_id=order_data.user_id,
        cargo_address=order_data.cargo_address,
        amount=order_data.amount,
        status=order_data.status)
    db.add(order)
    db.flush()
    for item in order_data.items:
        db_item = OrderItem(
            order_id=order.id,
            product_item=item.product_item,
            quantity=item.quantity,
            size_id=item.size_id,
            color_id=item.color_id)
        db.add(db_item)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()

# crud/payment_crud.py


def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
    payment = Payment(
        user_id=payment_data.user_id,
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        is_paid=payment_data.is_paid
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int) -> Payment:
    return db.query(Payment).filter(Payment.id == payment_id).first()

# crud/size_crud.py


def create_size(db: Session, size_data: SizeCreate) -> Size:
    size = Size(
        size_name=size_data.size_name,
        size_priority=size_data.size_priority)
    db.add(size)
    db.commit()
    db.refresh(size)
    return size


def get_size(db: Session, size_id: int) -> Size:
    return db.query(Size).filter(Size.id == size_id).first()

# crud/stock_crud.py


def create_size_stock(db: Session, size_stock_data: SizeStockCreate):
    size_stock = SizeStock(
        product_item=size_stock_data.product_item,
        size_id=size_stock_data.size_id,
        quantity=size_stock_data.quantity)
    db.add(size_stock)
    db.commit()
    db.refresh(size_stock)
    return size_stock


def create_color_stock(db: Session, color_stock_data: ColorStockCreate):
    color_stock = ColorStock(
        product_item=color_stock_data.product_item,
        color_id=color_stock_data.color_id,
        quantity=color_stock_data.quantity
    )
    db.add(color_stock)
    db.commit()
    db.refresh(color_stock)
    return color_stock

# crud/product_crud.py


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(name=product_data.name)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_color(db: Session, color_data: ColorCreate) -> Color:
    color = Color(name=color_data.name)
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def get_user_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_user_payments(db: Session, user_id: int) -> list[Payment]:
    return db.query(Payment).filter(Payment.user_id == user_id).all()
