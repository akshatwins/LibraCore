from datetime import datetime
from ..extensions import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(100), nullable=False)
    entity = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    actor = db.relationship("User")
