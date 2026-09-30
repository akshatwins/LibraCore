from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from ..extensions import db
from ..models import User

members_bp = Blueprint("members", __name__, url_prefix="/members")

@members_bp.get("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    query = User.query.filter(User.role == "member")
    if q:
        term = f"%{q}%"
        query = query.filter(or_(User.name.ilike(term), User.email.ilike(term)))
    members = query.order_by(User.name.asc()).all()
    return render_template("members/index.html", members=members, q=q)

@members_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role not in {"admin", "librarian"}:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "warning")
            return redirect(url_for("members.create"))
        member = User(
            name=request.form["name"].strip(),
            email=email,
            role="member"
        )
        member.set_password(request.form["password"])
        db.session.add(member)
        db.session.commit()
        flash("Member created successfully.", "success")
        return redirect(url_for("members.index"))
    return render_template("members/form.html")
