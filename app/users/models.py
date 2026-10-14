import uuid

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=func.uuidv7(monotonic=True), index=True
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"
