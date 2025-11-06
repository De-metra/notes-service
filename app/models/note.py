from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base,int_pk, str_null_true


class Note(Base):
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str_null_true]
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return self.title[:50]+"..."