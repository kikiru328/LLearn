from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class CurriculumModel(Base):
    __tablename__ = "curriculums"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    title = Column(String(100), nullable=False)
    goal = Column(String(500), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    # 1:N 관계
    weeks = relationship("WeekTopicModel", back_populates="curriculum", cascade="all, delete-orphan")