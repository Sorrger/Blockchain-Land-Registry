from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.database.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.crud.user import (
    create_user,
    get_user_by_wallet,
    get_user,
    get_users,
)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    existing = get_user_by_wallet(db, payload.wallet_address)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this wallet already exists",
        )

    user = User(
        id=uuid.uuid4(),
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        pesel=payload.pesel,
        wallet_address=payload.wallet_address,
    )

    return create_user(db, user)

@router.get("", response_model=list[UserRead])
def get_users_endpoint(
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
