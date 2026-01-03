from sqlalchemy.orm import Session
from app.models.user import User
import uuid

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_wallet(db: Session, wallet: str) -> User | None:
    return db.query(User).filter(User.wallet_address == wallet).first()


def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()