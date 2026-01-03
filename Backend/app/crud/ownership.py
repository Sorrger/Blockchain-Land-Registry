from sqlalchemy.orm import Session
from app.models.ownership import Ownership
from app.enums.txStatus import TxStatus
from datetime import datetime
import uuid


def create_ownership(
    db: Session,
    property_id: uuid.UUID,
    owner_id: uuid.UUID,
    tx_hash: str,
):
    db.query(Ownership).filter(
        Ownership.property_id == property_id,
        Ownership.to_date.is_(None)
    ).update({"to_date": datetime.utcnow()})

    ownership = Ownership(
        property_id=property_id,
        owner_id=owner_id,
        tx_hash=tx_hash,
        tx_status=TxStatus.pending,
    )

    db.add(ownership)
    db.commit()
    db.refresh(ownership)
    return ownership


def update_tx_status(
    db: Session,
    ownership: Ownership,
    status: TxStatus,
):
    ownership.tx_status = status
    db.commit()
    db.refresh(ownership)
    return ownership

def get_current_owner(db: Session, property_id: uuid.UUID) -> Ownership | None:
    return db.query(Ownership).filter(
        Ownership.property_id == property_id,
        Ownership.to_date.is_(None),
        Ownership.tx_status == TxStatus.confirmed
    ).first()

def get_ownership_history(db: Session, property_id: uuid.UUID):
    return db.query(Ownership).filter(
        Ownership.property_id == property_id
    ).order_by(Ownership.from_date.desc()).all()
