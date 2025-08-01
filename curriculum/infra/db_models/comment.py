from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curriculum.infra.db_models.curriculum import CurriculumModel
    from user.infra.db_models.user import UserModel


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    curriculum_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_comment_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 인덱스 설정 - 성능 최적화
    __table_args__ = (
        Index("idx_curriculum_created", "curriculum_id", "created_at"),
        Index("idx_parent_created", "parent_comment_id", "created_at"),
        Index("idx_user_created", "user_id", "created_at"),
        Index("idx_curriculum_deleted", "curriculum_id", "is_deleted"),
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

    # 자기 참조 관계 (대댓글)
    parent_comment: Mapped["CommentModel"] = relationship(
        "CommentModel",
        remote_side="CommentModel.id",
        passive_deletes=True,
    )
    replies: Mapped[list["CommentModel"]] = relationship(
        "CommentModel",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
