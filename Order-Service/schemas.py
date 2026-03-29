from typing import List, Optional
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    item_id: int = Field(..., example=101)
    item_name: str = Field(..., example="Chicken Kottu")
    quantity: int = Field(..., example=2)
    price: float = Field(..., example=1200.0)


class OrderCreate(BaseModel):
    user_id: int = Field(..., example=1)
    restaurant_id: int = Field(..., example=1)
    items: List[OrderItem]
    total_amount: float = Field(..., example=2400.0)


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, example="Confirmed")


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    items: str
    total_amount: float
    status: str

    class Config:
        from_attributes = True