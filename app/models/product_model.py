from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    # subcategory = Column('Subcategory', ForeignKey)