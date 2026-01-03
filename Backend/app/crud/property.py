from sqlalchemy.orm import Session
from app.models.property import Property
import uuid


def create_property(db: Session, prop: Property):
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


def get_property(db: Session, property_id: uuid.UUID):
    return db.query(Property).filter(Property.id == property_id).first()

def get_all_properties(db: Session):
    return db.query(Property).all()

def mark_property_onchain(
    db: Session,
    prop: Property,
    token_id: int,
    contract_address: str,
    mint_tx_hash: str,
):
    prop.token_id = token_id
    prop.contract_address = contract_address
    prop.mint_tx_hash = mint_tx_hash
    prop.is_onchain = True
    db.commit()
    db.refresh(prop)
    return prop

