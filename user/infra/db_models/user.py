from datetime import datetime
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
