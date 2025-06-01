from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.db.database import Base
from sqlalchemy.orm import relationship

from app.models.accounts import Currency, SubCategory


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    title = Column(String(50))
    description = Column(String)
    percentage = Column(Integer)

    subcategory = relationship(SubCategory, back_populates='products')
    product_prices = relationship('ProductPrice', back_populates='product')
    product_items = relationship('ProductItem', back_populates='product')


class ProductPrice(Base):
    __tablename__ = 'product_prices'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    currencies_id = Column(Integer, ForeignKey('currency.id'))
    price = Column(Numeric)
    amount = Column(Numeric)

    product = relationship(Product, back_populates='product_prices')
    currency = relationship(Currency, back_populates='product_prices')


class ProductItem(Base):
    __tablename__ = 'product_items'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    code = Column(String(20))

    product = relationship(Product, back_populates='product_items')
    product_images = relationship('ProductImage', back_populates='product_item')


class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True)
    product_item_id = Column(Integer, ForeignKey('product_items.id'))
    color_id = Column(Integer, ForeignKey('colors.id'))
    image = Column(String)

    product_item = relationship(ProductItem, back_populates='product_images')
    color = relationship("Color", back_populates='product_image_color')


class Color(Base):
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True)
    color_name = Column(String(80))
    color_code = Column(String(80))

    product_image_color = relationship('ProductImage', back_populates='color')
