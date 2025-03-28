from typing import List

from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):

    model_config = ConfigDict(strict=True)

    id:int
    name:str
    email:EmailStr|None = None
    password: bytes
    active:bool = True


class UserRegSchema(BaseModel):
    name:str
    email:EmailStr
    password: str|bytes

class TokenInfo(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str= 'Bearer'

class Item(BaseModel):
    product_id: int
    quantity: int
    item_total: int

class Order(BaseModel):
    items: List[Item]
    total: int
    receivedAmount: int
    change: int

