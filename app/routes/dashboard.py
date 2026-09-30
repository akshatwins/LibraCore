from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Circulation
from ..services.dashboard import metrics
from ..models import Notification
from ..services.notifications import generate_due_notifications

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/")
@login_required
def index():
    generate_due_notifications()
    recent = Circulation.query.order_by(Circulation.issued_at.desc()).limit(8).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    return render_template("dashboard/index.html", metrics=metrics(), recent=recent, notifications=notifications)
