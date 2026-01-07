from pydantic import BaseModel
import uuid

class PropertyCreate(BaseModel):
    property_number: str
    address: str
    area: float

class PropertyResponse(PropertyCreate):
    id: uuid.UUID  # <--- Change this from 'str' to 'uuid.UUID'
    token_id: int | None
    contract_address: str | None
    mint_tx_hash: str | None
    is_onchain: bool
    
    class Config:
        from_attributes = True

class PropertyOnChainStatus(BaseModel):
    token_id: int | None
    is_onchain: bool
    contract_address: str | None

    class Config:
        from_attributes = True

class PropertyWithOwner(PropertyResponse):
    current_owner_wallet: str | None


class PropertyMinted(BaseModel):
    token_id: int
    contract_address: str
    mint_tx_hash: str

    class Config:
        from_attributes = True