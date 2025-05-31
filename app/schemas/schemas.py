from pydantic import BaseModel
from app.models.models import Role

class UserBase(BaseModel):
    username: str

class UserRegister(UserBase):
    password: str
    role: Role

class UserLogin(UserBase): 
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access: str
    refresh: str
    token_type: str
