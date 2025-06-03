from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductPriceBase(BaseModel):
    currencies_id: int
    price: float

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPriceOut(ProductPriceBase):
    id: int
    amount: float
    class Config:
        orm_mode = True

class ProductImageBase(BaseModel):
    color_id: int
    image: str

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageOut(ProductImageBase):
    id: int
    product_item_id: int
    class Config:
        orm_mode = True

class SizeStockBase(BaseModel):
    size_id: int
    quantity: int

class SizeStockCreate(SizeStockBase):
    pass

class SizeStockOut(SizeStockBase):
    id: int
    class Config:
        orm_mode = True

class ColorStockBase(BaseModel):
    color_id: int
    quantity: int

class ColorStockCreate(ColorStockBase):
    pass

class ColorStockOut(ColorStockBase):
    id: int
    class Config:
        orm_mode = True

class ProductItemBase(BaseModel):
    code: str

class ProductItemCreate(ProductItemBase):
    images: List[ProductImageCreate]
    size_stocks: List[SizeStockCreate]
    color_stocks: List[ColorStockCreate]

class ProductItemOut(ProductItemBase):
    id: int
    product_id: int
    images: List[ProductImageOut]
    size_stocks: List[SizeStockOut]
    color_stocks: List[ColorStockOut]
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    percentage: Optional[int] = 0
    subcategory_id: int

class ProductCreate(ProductBase):
    prices: List[ProductPriceCreate]
    items: List[ProductItemCreate]

class ProductOut(ProductBase):
    id: int
    amount: Optional[float] = None
    prices: List[ProductPriceOut]
    items: List[ProductItemOut]
    class Config:
        orm_mode = True

class ColorBase(BaseModel):
    color_name: str
    color_code: str

class ColorCreate(ColorBase):
    pass

class ColorOut(ColorBase):
    id: int
    class Config:
        orm_mode = True

class SizeBase(BaseModel):
    size_name: str
    size_priority: int

class SizeCreate(SizeBase):
    pass

class SizeOut(SizeBase):
    id: int
    class Config:
        orm_mode = True