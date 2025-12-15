from pydantic import BaseModel
import uuid
from datetime import datetime


class PropertyCreate(BaseModel):
    property_number: str
    address: str
    area: float


class PropertyRead(BaseModel):
    id: uuid.UUID
    property_number: str
    address: str
    area: float
    created_at: datetime


class Config:
    from_attributes = True