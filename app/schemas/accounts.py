from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    adress: str


class UserRegister(UserBase):
    password: str


class UserLogin(UserRegister):
    pass


class UserOut(UserBase):
    id: int

    class Confing:
        orm_mode = True


class Token(BaseModel):
    access: str
    refresh: str
    token_type: str


class CountryBase(BaseModel):
    title: str
    is_active: bool


class CountryOut(CountryBase):
    id: int

    class Config:
        orm_mode = True


class CurrencyBase(BaseModel):
    country_id: int
    currency_rate: int


class CurrencyOut(CurrencyBase):
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    description: str
    image: str
    is_active: bool


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class SubCategoryBase(UserBase):
    category_id: int
    title: str
    description: str
    iamge: str
    is_active: bool


class SubCategoryOut(SubCategoryBase):
    id: int

    class Config:
        orm_mode = True
