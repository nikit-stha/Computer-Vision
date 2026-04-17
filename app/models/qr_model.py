import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db



class QR(db.Model):
    __tablename__ = "qr"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"))
    data: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True)

    user: so.Mapped["User"] = so.relationship(back_populates="qr_codes")