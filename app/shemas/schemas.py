from typing import List
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





class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None