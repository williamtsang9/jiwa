from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


STATUS_BACKLOG = "backlog"
STATUS_TO_BE_STARTED = "to_be_started"
STATUS_IN_PROGRESS = "in_progress"
STATUS_NEEDS_REVIEWING = "needs_reviewing"
STATUS_MERGED = "merged"
STATUS_COMPLETED = "completed"

ALLOWED_STATUSES = [
    STATUS_BACKLOG,
    STATUS_TO_BE_STARTED,
    STATUS_IN_PROGRESS,
    STATUS_NEEDS_REVIEWING,
    STATUS_MERGED,
    STATUS_COMPLETED,
]

BOARD_STATUSES = [
    STATUS_TO_BE_STARTED,
    STATUS_IN_PROGRESS,
    STATUS_NEEDS_REVIEWING,
    STATUS_MERGED,
    STATUS_COMPLETED,
]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=STATUS_BACKLOG)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
