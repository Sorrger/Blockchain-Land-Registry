from pydantic import BaseModel, field_validator
from datetime import datetime
from app.enums.txStatus import TxStatus
import uuid

class OwnershipCreate(BaseModel):
    property_id: str
    owner_wallet: str

    @field_validator("owner_wallet")
    def validate_wallet(cls, v):
        if not v.startswith("0x") or len(v) != 42:
            raise ValueError("Invalid Ethereum address")
        return v.lower()

class OwnerRead(BaseModel):
    wallet_address: str
    first_name: str | None
    last_name: str | None

    class Config:
        from_attributes = True

class OwnershipResponse(BaseModel):
    id: uuid.UUID # <--- Change from 'str' to 'uuid.UUID'
    property_id: uuid.UUID # <--- Change from 'str' to 'uuid.UUID'
    # owner: OwnerRead # (If you are using nested models, ensure they match too)
    tx_hash: str
    tx_status: TxStatus
    # ... other fields

    class Config:
        from_attributes = True


class OwnershipUpdateTx(BaseModel):
    tx_status: TxStatus
    to_date: datetime | None = None

    class Config:
        from_attributes = True

