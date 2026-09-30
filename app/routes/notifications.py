from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Notification

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.post("/<int:notification_id>/read")
@login_required
def mark_read(notification_id):
    item = db.session.get(Notification, notification_id)
    if item and item.user_id == current_user.id:
        item.is_read = True
        db.session.commit()
    return redirect(url_for("dashboard.index"))
