from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database.deps import get_db
from app.schemas.ownership import OwnershipCreate, OwnershipResponse
from app.crud.ownership import create_ownership
from app.crud.user import get_user_by_wallet
from app.crud.property import get_property

router = APIRouter(
    prefix="/ownerships",
    tags=["ownerships"]
)


@router.post("/", response_model=OwnershipResponse, status_code=status.HTTP_201_CREATED)
def create_ownership_endpoint(
    payload: OwnershipCreate,
    db: Session = Depends(get_db),
):
    prop = get_property(db, uuid.UUID(payload.property_id))
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    owner = get_user_by_wallet(db, payload.owner_wallet)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    ownership = create_ownership(
        db=db,
        property_id=prop.id,
        owner_id=owner.id,
        tx_hash="0xPENDING",
    )

    return ownership
