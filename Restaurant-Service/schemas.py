from typing import Optional, List
from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    item_name: str = Field(..., example="Chicken Burger")
    price: float = Field(..., example=1200.00)
    description: Optional[str] = Field(None, example="Spicy chicken burger")


class MenuItemUpdate(BaseModel):
    item_name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class MenuItemResponse(BaseModel):
    id: int
    item_name: str
    price: float
    description: Optional[str] = None
    restaurant_id: int

    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    name: str = Field(..., example="Food Hub")
    location: str = Field(..., example="Colombo")
    contact: str = Field(..., example="0771234567")
    cuisine: Optional[str] = Field(None, example="Sri Lankan")


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    cuisine: Optional[str] = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str
    contact: str
    cuisine: Optional[str] = None

    class Config:
        from_attributes = True


class RestaurantWithMenuResponse(BaseModel):
    id: int
    name: str
    location: str
    contact: str
    cuisine: Optional[str] = None
    menu_items: List[MenuItemResponse] = []

    class Config:
        from_attributes = True