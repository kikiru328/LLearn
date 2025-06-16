from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class LikeModel(Base):
    __tablename__ = "likes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    target_type = Column(String(20), nullable=False)   # 'summary' or 'curriculum'
    target_id = Column(PG_UUID(as_uuid=True), nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'target_type', 'target_id', name='uq_like_user_target'),
    )