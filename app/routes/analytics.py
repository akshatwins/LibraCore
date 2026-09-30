from flask import Blueprint, render_template
from flask_login import login_required
from ..services.analytics import analytics

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.get("/")
@login_required
def index():
    return render_template("analytics/index.html", data=analytics())
