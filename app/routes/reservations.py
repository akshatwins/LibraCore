from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..models import Reservation
from ..services.reservations import reserve_book, cancel_reservation, ReservationError

reservations_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

@reservations_bp.get("/")
@login_required
def index():
    if current_user.role == "member":
        items = Reservation.query.filter_by(member_id=current_user.id).order_by(Reservation.reserved_at.desc()).all()
    else:
        items = Reservation.query.order_by(Reservation.reserved_at.desc()).all()
    return render_template("reservations/index.html", reservations=items)

@reservations_bp.post("/book/<int:book_id>")
@login_required
def create(book_id):
    try:
        reserve_book(book_id, current_user.id)
        flash("Reservation placed successfully.", "success")
    except ReservationError as exc:
        flash(str(exc), "warning")
    return redirect(url_for("books.index"))

@reservations_bp.post("/<int:reservation_id>/cancel")
@login_required
def cancel(reservation_id):
    try:
        cancel_reservation(reservation_id, current_user.id)
        flash("Reservation cancelled.", "success")
    except ReservationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("reservations.index"))
