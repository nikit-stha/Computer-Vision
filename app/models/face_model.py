import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Face(db.Model):
    __tablename__ = "face"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"))
    encoding: so.Mapped[str] = so.mapped_column(sa.Text)

    user: so.Mapped["User"] = so.relationship(back_populates="faces")