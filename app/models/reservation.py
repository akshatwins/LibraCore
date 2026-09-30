from datetime import datetime
from ..extensions import db

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fulfilled_at = db.Column(db.DateTime)

    book = db.relationship("Book", back_populates="reservations")
    member = db.relationship("User", back_populates="reservations")
