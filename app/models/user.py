from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="member")
    is_active_user = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    loans = db.relationship("Circulation", back_populates="member", foreign_keys="Circulation.member_id")
    reservations = db.relationship("Reservation", back_populates="member", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    fine_payments = db.relationship("FinePayment", back_populates="member", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.is_active_user

    def can_manage(self):
        return self.role in {"admin", "librarian"}

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
