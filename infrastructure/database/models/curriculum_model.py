from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import BaseModel

class CurriculumModel(BaseModel):
    """curriculum SQLAlchemy model"""
    __tablename__ = "curriculums"
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        comment="사용자 ID"
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="커리큘럼 제목"
    )

    goal: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="학습 목표"
    )

    duration_weeks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="커리큘럼 주차"
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True, # lot of query
        comment="공개 상태"
    )
