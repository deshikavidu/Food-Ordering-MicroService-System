from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    full_name: str = Field(..., example="Nimal Perera")
    email: EmailStr = Field(..., example="nimal@gmail.com")
    password: str = Field(..., example="123456")
    phone: Optional[str] = Field(None, example="0771234567")
    address: Optional[str] = Field(None, example="Colombo")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="nimal@gmail.com")
    password: str = Field(..., example="123456")


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True