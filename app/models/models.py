from sqlalchemy import String, Integer, Enum, Column, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime

from app.db.database import Base
from app.models.accounts import User
from app.models.product_model import Product, Color

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cargo_address = Column(String(255))
    amount = Column(Float)

    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)


class Size(Base):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True)
    size_name = Column(String(10))
    size_priority = Column(Integer)


class SizeStock(Base):
    __tablename__ = 'size_stocks'

    id = Column(Integer, primary_key=True)
    product_item = Column(Integer, ForeignKey('products.id'))
    size_id = Column(Integer, ForeignKey('sizes.id'))
    quantity = Column(Integer)

    product = relationship("Product", backref="size_stocks")
    size = relationship("Size", backref="size_stocks")


class ColorStock(Base):
    __tablename__ = 'color_stocks'

    id = Column(Integer, primary_key=True)
    product_item = Column(Integer, ForeignKey('products.id'))
    color_id = Column(Integer, ForeignKey('colors.id'))
    quantity = Column(Integer)

    product = relationship("Product", backref="color_stocks")
    color = relationship("Color", backref="color_stocks")


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    is_paid = Column(Boolean, default=False)

    user = relationship("User", backref="payments")
    order = relationship("Order", back_populates="payment")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    size_id = Column(Integer, ForeignKey('sizes.id'))
    color_id = Column(Integer, ForeignKey('colors.id'))

    order = relationship("Order", back_populates="items")
    product = relationship("Product", backref="order_items")
    size = relationship("Size", backref="order_items")
    color = relationship("Color", backref="order_items")