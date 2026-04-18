import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Quiz(db.Model):

    __tablename__ = "quiz"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    question: so.Mapped[str] = so.mapped_column(sa.String(512), unique=True)

    option1 : so.Mapped[str] = so.mapped_column(sa.String(128))
    option2 : so.Mapped[str] = so.mapped_column(sa.String(128))
    option3 : so.Mapped[str] = so.mapped_column(sa.String(128))
    option4 : so.Mapped[str] = so.mapped_column(sa.String(128))

    answer  : so.Mapped[int] = so.mapped_column(index=True)