from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class SummaryModel(Base):
    __tablename__ = "summaries"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    curriculum_id = Column(PG_UUID(as_uuid=True), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False)

    week_number = Column(Integer, nullable=False)
    content = Column(String(3000), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    # 관계
    user = relationship("UserModel", backref="summaries")
    curriculum = relationship("CurriculumModel", backref="summaries")
    feedback = relationship("FeedbackModel", back_populates="summary", uselist=False)
