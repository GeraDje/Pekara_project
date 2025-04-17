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

