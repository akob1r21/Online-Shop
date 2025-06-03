from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

# schemas/order_schemas.py


class OrderItemBase(BaseModel):
    product_item: int
    quantity: int
    size_id: int
    color_id: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderStatusEnum(str, Enum):
    accepted = "қабул шуд"
    on_the_way = "дар роҳ"
    delivered = "расид"


class OrderBase(BaseModel):
    cargo_address: str
    amount: float
    status: OrderStatusEnum = OrderStatusEnum.accepted


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    id: int
    items: List[OrderItemRead]

    class Config:
        orm_mode = True

# schemas/payment_schemas.py


class PaymentBase(BaseModel):
    user_id: int
    order_id: int
    amount: float
    is_paid: bool = False


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# schemas/stock_schemas.py


class SizeStockBase(BaseModel):
    product_item: int
    size_id: int
    quantity: int


class SizeStockCreate(SizeStockBase):
    pass


class SizeStockRead(SizeStockBase):
    id: int

    class Config:
        orm_mode = True


class ColorStockBase(BaseModel):
    product_item: int
    color_id: int
    quantity: int


class ColorStockCreate(ColorStockBase):
    pass


class ColorStockRead(ColorStockBase):
    id: int

    class Config:
        orm_mode = True

# schemas/product_schemas.py


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ColorBase(BaseModel):
    name: str


class ColorCreate(ColorBase):
    pass


class ColorRead(ColorBase):
    id: int

    class Config:
        orm_mode = True


class SizeBase(BaseModel):
    size_name: str
    size_priority: int


class SizeCreate(SizeBase):
    pass


class SizeRead(SizeBase):
    id: int

    class Config:
        orm_mode = True
