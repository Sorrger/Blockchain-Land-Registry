# app/routers/ownerships.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
import uuid

from app.database.deps import get_db
from app.schemas.ownership import OwnershipCreate, OwnershipResponse
from app.crud.ownership import create_ownership
from app.crud.user import get_user_by_wallet
from app.crud.property import get_property, mark_property_onchain
# Import BOTH blockchain functions
from app.blockchain.land_register import register_property_on_chain, transfer_property_on_chain
from app.enums.txStatus import TxStatus
from app.core.config import settings
from web3 import Web3

router = APIRouter(
    prefix="/ownerships",
    tags=["ownerships"]
)

@router.post("/", response_model=OwnershipResponse, status_code=status.HTTP_201_CREATED)
def change_ownership_endpoint(
    payload: OwnershipCreate,
    x_role: str = Header(default="user"), # Simple security check
    db: Session = Depends(get_db),
):
    # 0. Security Check
    if x_role != "notary":
        raise HTTPException(status_code=403, detail="Only a Notary can transfer ownership.")

    # 1. Validate inputs
    try:
        prop_uuid = uuid.UUID(payload.property_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Property ID format")

    prop = get_property(db, prop_uuid)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    owner = get_user_by_wallet(db, payload.owner_wallet)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found. Register user first.")

    tx_hash = "0xPENDING"
    tx_status = TxStatus.pending

    try:
        # 2. CASE A: Property is NOT on-chain yet -> REGISTER IT
        if not prop.is_onchain:
            print(f"Blockchain: Registering {prop.property_number}...")
            
            # Create a real data hash from address + area
            data_str = f"{prop.address}-{prop.area}"
            data_hash = Web3.keccak(text=data_str)

            tx_hash = register_property_on_chain(
                kw_id=prop.property_number,
                data_hash=data_hash,
                owner=payload.owner_wallet
            )
            
            # Mark as on-chain in DB
            mark_property_onchain(
                db=db,
                prop=prop,
                token_id=0,
                contract_address=settings.CONTRACT_ADDRESS,
                mint_tx_hash=tx_hash
            )
            
        # 3. CASE B: Property IS on-chain -> TRANSFER IT
        else:
            print(f"Blockchain: Transferring {prop.property_number}...")
            tx_hash = transfer_property_on_chain(
                kw_id=prop.property_number,
                new_owner_wallet=payload.owner_wallet
            )

        print(f"Success! Hash: {tx_hash}")
        tx_status = TxStatus.confirmed

    except Exception as e:
        print(f"Blockchain Error: {e}")
        # We allow the DB update to happen even if chain fails? 
        # Usually no, but for debug let's fail.
        raise HTTPException(status_code=500, detail=f"Blockchain failed: {str(e)}")

    # 4. Save Record
    ownership = create_ownership(
        db=db,
        property_id=prop.id,
        owner_id=owner.id,
        tx_hash=tx_hash,
    )
    
    ownership.tx_status = tx_status
    db.commit()
    db.refresh(ownership)

    return ownership