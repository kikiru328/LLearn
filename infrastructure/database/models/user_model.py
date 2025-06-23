from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import BaseModel


class UserModel(BaseModel):
    """User SQLAlchemy 모델"""
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="사용자 이메일"
    )

    nickname: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="사용자 닉네임"
    )

    hashed_password: Mapped[str] = mapped_column(  # ← 수정!
        String(255),
        nullable=False,
        comment="해시된 비밀번호"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="활성 상태"
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="관리자 여부"
    )
