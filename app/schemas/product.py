from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    percentage: Optional[int] = None
    subcategory_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductItemsBase(BaseModel):
    product_id : int
    code: str



class ProductItemCreate(ProductItemsBase):
    pass


class ProductItemRead(ProductItemsBase):
    id: int

    class Config:
        orm_mode = True
        


class ProductPriceBase(BaseModel):
    product_id : int
    currencies_id: int
    price: int
    amount: int



class ProductPriceCreate(ProductPriceBase):
    pass


class ProductPriceRead(ProductPriceBase):
    id: int

    class Config:
        orm_mode = True
        
