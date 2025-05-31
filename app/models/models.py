from sqlalchemy import String, Integer, Enum, Column, Float, DateTime, Boolean

from enum import Enum as PyEnum
from datetime import datetime

from app.db.database import Base

from app.models.accounts import User
from app.models.product_model import Product, Color

class Order(Base):
    __tablename__='orders'

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, User.id)
    cargo_address=Column(String(255))
    amount=Column(Float)


class Size(Base):
    __tablename__='sizes'

    id=Column(Integer, primary_key=True)
    size_name=Column(String(10))
    size_priority=Column(Integer)


class SizeStock(Base):
    __tablename__='size_stocks'

    id=Column(Integer, primary_key=True)
    product_item=Column(Integer, Product.id)
    size=Column(Integer, Size.id)
    quantity=Column(Integer)


class ColorStock(Base):
    __tablename__='color_stocks'

    id=Column(Integer, primary_key=True)
    product_item=Column(Integer, Product.id)
    color=Column(Integer, Color.id)
    quantity=Column(Integer)


class Payment(Base):
    __tablename__='payments'

    id=Column(Integer, primary_key=True)
    user=Column(Integer, User.id)
    order=Column(Integer, Order.id)
    amount=Column(Float)
    created_at=Column(DateTime, default=datetime.now())
    is_paid=Column(Boolean, default=False)


class OrderItem(Base):
    __tablename__='order_items'

    id=Column(Integer, primary_key=True)
    order=Column(Integer, Order.id)
    product=Column(Integer, Product.id)
    quantity=Column(Integer)
    size=Column(Integer, Size.id)
    color=Column(Integer, Color.id)