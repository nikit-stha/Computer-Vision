import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256))

    qr_codes: so.Mapped[list["QR"]] = so.relationship(back_populates="user")
    faces: so.Mapped[list["Face"]] = so.relationship(back_populates="user")