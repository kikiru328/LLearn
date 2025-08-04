from datetime import datetime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from app.common.db.database import Base
from app.modules.user.domain.vo.role import RoleVO


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[RoleVO] = mapped_column(
        SQLEnum(RoleVO, name="user_role"), default=RoleVO.USER, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
