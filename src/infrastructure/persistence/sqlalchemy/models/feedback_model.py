from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class FeedbackModel(Base):
    __tablename__ = "feedbacks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary_id = Column(PG_UUID(as_uuid=True), ForeignKey("summaries.id", ondelete="CASCADE"), nullable=False)

    reviewer = Column(String(50), nullable=False, default="LLM")
    content = Column(String(2000), nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    summary = relationship("SummaryModel", back_populates="feedback")