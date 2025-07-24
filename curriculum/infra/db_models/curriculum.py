from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base


class CurriculumModel(Base):
    __tablename__ = "curriculums"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 관계 설정
    owner = relationship("User", back_populates="curriculums")
    week_schedules = relationship(
        "WeekScheduleModel",
        back_populates="curriculum",
        cascade="all, delete-orphan",
    )


class WeekScheduleModel(Base):
    __tablename__ = "week_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    topics: Mapped[list] = mapped_column(JSON, nullable=False)

    curriculum = relationship("CurriculumModel", back_populates="week_schedules")
    summaries = relationship(
        "SummaryModel",
        back_populates="week_schedule",
        cascade="all, delete-orphan",
    )


class SummaryModel(Base):
    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    curriculum_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    week_schedule_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("week_schedules.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    week_schedule = relationship("WeekScheduleModel", back_populates="summaries")
    feedbacks = relationship(
        "FeedbackModel",
        back_populates="summary",
        cascade="all, delete-orphan",
    )


class FeedbackModel(Base):
    __tablename__ = "feedbacks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    summary_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("summaries.id", ondelete="CASCADE"), nullable=False
    )
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    summary = relationship("SummaryModel", back_populates="feedbacks")
