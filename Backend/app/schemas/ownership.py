from pydantic import BaseModel, field_validator
from datetime import datetime
from app.enums.txStatus import TxStatus

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
    id: str
    property_id: str
    owner: OwnerRead
    tx_hash: str
    tx_status: TxStatus
    from_date: datetime
    to_date: datetime | None

    class Config:
        from_attributes = True


class OwnershipUpdateTx(BaseModel):
    tx_status: TxStatus
    to_date: datetime | None = None

    class Config:
        from_attributes = True

