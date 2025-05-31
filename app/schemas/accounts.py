from pydantic import BaseModel




class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserRegister(UserBase):
    password: str

class UserLogin(UserRegister):
    pass

class UserOut(UserBase):
    id: int

class Token(BaseModel):
    access: str
    refresh: str
    token_type: str
    
