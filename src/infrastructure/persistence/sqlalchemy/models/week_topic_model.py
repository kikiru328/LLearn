from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from infrastructure.persistence.sqlalchemy.base import Base

class WeekTopicModel(Base):
    __tablename__ = "week_topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id = Column(PG_UUID(as_uuid=True), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False)

    week_number = Column(Integer, nullable=False)
    topic = Column(String(255), nullable=False)

    curriculum = relationship("CurriculumModel", back_populates="weeks")
