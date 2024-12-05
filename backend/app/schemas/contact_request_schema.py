from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactRequestBase(BaseModel):
    vehicle_id: int
    user_id: Optional[int] = None

class ContactRequestCreate(ContactRequestBase):
    pass

class ContactRequestResponse(ContactRequestBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
