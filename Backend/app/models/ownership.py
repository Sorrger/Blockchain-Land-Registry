import uuid
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.session import Base
from sqlalchemy.orm import relationship
from app.enums.txStatus import TxStatus

class Ownership(Base):
    __tablename__ = "ownerships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    property_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("properties.id"))
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    from_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    to_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    tx_hash: Mapped[str] = mapped_column(String(66))
    tx_status: Mapped[TxStatus] = mapped_column(default=TxStatus.pending)


    property = relationship("Property", back_populates="ownerships")
    owner = relationship("User")
