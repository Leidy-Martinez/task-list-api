from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    __tablename__ = 'goal'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
