from pydantic import BaseModel
import uuid
from datetime import datetime


class OwnershipCreate(BaseModel):
    property_id: uuid.UUID
    to_owner_id: uuid.UUID


class OwnershipRead(BaseModel):
    id: uuid.UUID
    property_id: uuid.UUID
    owner_id: uuid.UUID
    from_date: datetime
    to_date: datetime | None
    tx_hash: str


class Config:
    from_attributes = True