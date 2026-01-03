import uuid
from sqlalchemy import String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.session import Base
from sqlalchemy.orm import relationship

class Property(Base):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # OFF-CHAIN
    property_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    address: Mapped[str] = mapped_column(String(255))
    area: Mapped[float] = mapped_column(Float)

    # ON-CHAIN
    token_id: Mapped[int | None] = mapped_column(nullable=True)
    contract_address: Mapped[str | None] = mapped_column(String(42))
    mint_tx_hash: Mapped[str | None] = mapped_column(String(66))
    is_onchain: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ownerships = relationship("Ownership", back_populates="property")