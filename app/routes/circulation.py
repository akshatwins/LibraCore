from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..models import Book, User, Circulation
from ..services.circulation import issue_book, return_book, renew_book, CirculationError

circulation_bp = Blueprint("circulation", __name__, url_prefix="/circulation")

@circulation_bp.get("/")
@login_required
def index():
    active = Circulation.query.filter_by(returned_at=None).order_by(Circulation.due_date.asc()).all()
    history = Circulation.query.filter(Circulation.returned_at.is_not(None)).order_by(Circulation.returned_at.desc()).limit(20).all()
    return render_template("circulation/index.html", active=active, history=history)

@circulation_bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue():
    if current_user.role not in {"admin", "librarian"}:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        try:
            issue_book(int(request.form["book_id"]), int(request.form["member_id"]), current_user.id)
            flash("Book issued successfully.", "success")
            return redirect(url_for("circulation.index"))
        except (ValueError, CirculationError) as exc:
            flash(str(exc), "danger")
    books = Book.query.filter(Book.available_copies > 0).order_by(Book.title).all()
    members = User.query.filter_by(role="member", is_active_user=True).order_by(User.name).all()
    return render_template("circulation/form.html", books=books, members=members)

@circulation_bp.post("/<int:loan_id>/return")
@login_required
def return_loan(loan_id):
    if current_user.role not in {"admin", "librarian"}:
        return redirect(url_for("dashboard.index"))
    try:
        loan = return_book(loan_id, current_user.id)
        flash(f"Book returned. Fine: ₹{loan.fine_amount:.2f}", "success")
    except CirculationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("circulation.index"))

@circulation_bp.post("/<int:loan_id>/renew")
@login_required
def renew(loan_id):
    if current_user.role not in {"admin", "librarian"}:
        return redirect(url_for("dashboard.index"))
    try:
        renew_book(loan_id, current_user.id)
        flash("Loan renewed successfully.", "success")
    except CirculationError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("circulation.index"))
