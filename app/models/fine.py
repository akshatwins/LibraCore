from datetime import datetime
from ..extensions import db

class FinePayment(db.Model):
    __tablename__ = "fine_payments"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    circulation_id = db.Column(db.Integer, db.ForeignKey("circulation.id"))
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(40), default="cash", nullable=False)
    reference = db.Column(db.String(100))
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    member = db.relationship("User", back_populates="fine_payments")
    circulation = db.relationship("Circulation")
