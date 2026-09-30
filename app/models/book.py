from datetime import datetime
from ..extensions import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(220), nullable=False, index=True)
    author = db.Column(db.String(180), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    publisher = db.Column(db.String(180))
    publication_year = db.Column(db.Integer)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    shelf = db.Column(db.String(50))
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))
    language = db.Column(db.String(80), default="English")
    pages = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    loans = db.relationship("Circulation", back_populates="book", cascade="all, delete-orphan")
    reservations = db.relationship("Reservation", back_populates="book", cascade="all, delete-orphan")

    @property
    def availability_label(self):
        if self.available_copies <= 0:
            return "Unavailable"
        if self.available_copies <= 2:
            return "Low stock"
        return "Available"
