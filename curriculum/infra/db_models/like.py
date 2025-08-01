from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curriculum.infra.db_models.curriculum import CurriculumModel
    from user.infra.db_models.user import UserModel


class LikeModel(Base):
    __tablename__ = "likes"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    curriculum_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 한 유저가 같은 커리큘럼에 중복 좋아요 방지
    __table_args__ = (
        UniqueConstraint(
            "user_id", "curriculum_id", name="unique_user_curriculum_like"
        ),
    )

    # 관계 설정
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        passive_deletes=True,
    )
    curriculum: Mapped["CurriculumModel"] = relationship(
        "CurriculumModel",
        passive_deletes=True,
    )
