from typing import Optional
from pydantic import BaseModel

class DeliveryCreate(BaseModel):
    order_id: int
    driver_name: str
    status: Optional[str] = "Preparing"
    estimated_time: Optional[str] = None

class DeliveryUpdate(BaseModel):
    status: Optional[str] = None
    driver_name: Optional[str] = None
    estimated_time: Optional[str] = None

class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    driver_name: str
    status: str
    estimated_time: Optional[str] = None

    class Config:
        from_attributes = True