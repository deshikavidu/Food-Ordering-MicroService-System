from pydantic import BaseModel, Field
from typing import Optional


class PaymentCreate(BaseModel):
    order_id: int = Field(..., example=1)
    amount: float = Field(..., example=2400.0)
    method: str = Field(..., example="Card")


class PaymentUpdate(BaseModel):
    status: Optional[str] = Field(None, example="Refunded")


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    method: str
    status: str

    class Config:
        from_attributes = True