from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime
from ..db import db

class Task(db.Model):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)   # Title column required
    description: Mapped[str] = mapped_column(nullable=False)    # Description column required
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=None)
    is_complete: Mapped[Optional[bool]] = False