from datetime import datetime, date
from ..extensions import db

class Circulation(db.Model):
    __tablename__ = "circulation"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    returned_at = db.Column(db.DateTime)
    renewal_count = db.Column(db.Integer, default=0, nullable=False)
    fine_amount = db.Column(db.Float, default=0, nullable=False)

    book = db.relationship("Book", back_populates="loans")
    member = db.relationship("User", back_populates="loans")

    @property
    def status(self):
        if self.returned_at:
            return "Returned"
        if self.due_date < date.today():
            return "Overdue"
        return "Issued"

    @property
    def days_overdue(self):
        if self.returned_at:
            end = self.returned_at.date()
        else:
            end = date.today()
        return max(0, (end - self.due_date).days)
