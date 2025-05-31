from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.database import Base




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(200))
    first_name = Column(String(50))
    last_name = Column(String(50))
    adress = Column(String(100))
    phone_number = Column(String(15))
    email = Column(String(150), unique=True)
    role = Column(String(10))


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)

    currencies = relationship('Currency', back_populates='country')


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    currency_rate = Column(Integer)

    country = relationship('Country', back_populates='currencies')


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), unique=True)
    description = Column(Text)
    image = Column(String)
    is_active = Column(Boolean, default=True)

    subcategories = relationship('SubCategory', back_populates='category')


class SubCategory(Base):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    title = Column(String(60), unique=True)
    description = Column(Text)
    iamge = Column(String)
    is_active = Column(Boolean, default=True)

    category = relationship('Category', back_populates='subcategories')
