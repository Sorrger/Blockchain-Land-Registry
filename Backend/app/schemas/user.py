from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime
from pydantic import field_validator


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    pesel: str
    wallet_address: str
    @field_validator("wallet_address")
    def validate_wallet(cls, v):
        if not v.startswith("0x") or len(v) != 42:
            raise ValueError("Invalid Ethereum address")
        return v.lower()


class UserRead(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime


class Config:
    from_attributes = True