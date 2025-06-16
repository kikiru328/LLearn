from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    summary_id = Column(PG_UUID(as_uuid=True), ForeignKey("summaries.id", ondelete="CASCADE"), nullable=False)

    content = Column(String(1000), nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    user = relationship("UserModel", backref="comments")
    summary = relationship("SummaryModel", backref="comments")