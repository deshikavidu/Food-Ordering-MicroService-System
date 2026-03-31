from typing import Optional
from pydantic import BaseModel, field_validator
import re


class DeliveryCreate(BaseModel):
    order_id: int
    driver_name: str
    status: Optional[str] = "Preparing"
    estimated_time: Optional[str] = None

    @field_validator('order_id')
    @classmethod
    def validate_order_id(cls, v):
        if v <= 0:
            raise ValueError('order_id must be a positive number')
        return v

    @field_validator('driver_name')
    @classmethod
    def validate_driver_name(cls, v):
        if not v or not v.strip():
            raise ValueError('driver_name cannot be empty or whitespace')
        if not re.match(r'^[A-Za-z\s]+$', v.strip()):
            raise ValueError('driver_name must contain letters only, no numbers or symbols')
        if len(v.strip()) < 2:
            raise ValueError('driver_name must be at least 2 characters')
        return v.strip()

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['Preparing', 'Out for Delivery', 'Delivered', 'Cancelled']
            if v not in valid_statuses:
                raise ValueError(f'status must be one of: {", ".join(valid_statuses)}')
        return v

    @field_validator('estimated_time')
    @classmethod
    def validate_estimated_time(cls, v):
        if v is not None:
            if v.strip().lower() == 'string':
                raise ValueError('estimated_time must be a real value like "30 minutes" or "1hrs", not "string"')
            if len(v.strip()) < 2:
                raise ValueError('estimated_time must be a valid value')
        return v


class DeliveryUpdate(BaseModel):
    status: Optional[str] = None
    driver_name: Optional[str] = None
    estimated_time: Optional[str] = None

    @field_validator('driver_name')
    @classmethod
    def validate_driver_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('driver_name cannot be empty or whitespace')
            if not re.match(r'^[A-Za-z\s]+$', v.strip()):
                raise ValueError('driver_name must contain letters only, no numbers or symbols')
            if len(v.strip()) < 2:
                raise ValueError('driver_name must be at least 2 characters')
        return v.strip() if v else v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ['Preparing', 'Out for Delivery', 'Delivered', 'Cancelled']
            if v not in valid_statuses:
                raise ValueError(f'status must be one of: {", ".join(valid_statuses)}')
        return v

    @field_validator('estimated_time')
    @classmethod
    def validate_estimated_time(cls, v):
        if v is not None:
            if v.strip().lower() == 'string':
                raise ValueError('estimated_time must be a real value like "30 minutes" or "1hrs", not "string"')
            if len(v.strip()) < 2:
                raise ValueError('estimated_time must be a valid value')
        return v


class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    driver_name: str
    status: str
    estimated_time: Optional[str] = None

    class Config:
        from_attributes = True