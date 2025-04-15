from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Item(BaseModel):
    product_id: int
    quantity: int
    item_total: int

class Order(BaseModel):
    items: List[Item]
    total: int
    receivedAmount: int
    change: int


class UserRegister(BaseModel):
    name:str
    email: EmailStr
    password: str
    role_id:str








class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    roles: List[str]