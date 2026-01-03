from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database.deps import get_db
from app.schemas.property import PropertyCreate, PropertyResponse
from app.models.property import Property
from app.crud.property import create_property, get_property

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(
    payload: PropertyCreate,
    db: Session = Depends(get_db),
):
    prop = Property(
        id=uuid.uuid4(),
        property_number=payload.property_number,
        address=payload.address,
        area=payload.area,
        is_onchain=False,
    )

    return create_property(db, prop)


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property_endpoint(
    property_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    prop = get_property(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    return prop
