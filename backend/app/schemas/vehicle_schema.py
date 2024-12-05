from pydantic import BaseModel, Field
from typing import List, Optional

class VehicleBase(BaseModel):
    model: str = Field(..., min_length=2, max_length=100)
    type: str = Field(..., regex="^(car|truck|motorcycle)$")
    description: Optional[str] = None
    price: Optional[float] = None
    year: Optional[int] = None

class VehicleCreate(VehicleBase):
    seller_id: int
    images: Optional[List[str]] = []

class VehicleResponse(VehicleBase):
    id: int
    seller_id: int
    images: List[str]

    class Config:
        orm_mode = True

class VehicleSearchParams(BaseModel):
    vehicle_type: Optional[str] = None
    model: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
