from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampedModelMixin:
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("utc", func.now()),
        onupdate=func.timezone("utc", func.now()),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.timezone("utc", func.now())
    )
