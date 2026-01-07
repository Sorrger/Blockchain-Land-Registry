# app/schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator
import uuid
from datetime import datetime

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
    wallet_address: str  # <--- THIS WAS MISSING
    created_at: datetime

    class Config:
        from_attributes = True