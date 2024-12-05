from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=15)
    role: Optional[str] = "user"

class UserCreate(UserBase):
    @validator('mobile_number')
    def validate_mobile_number(cls, v):
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    mobile_number: str
    otp: str
