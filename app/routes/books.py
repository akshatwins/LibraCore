from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from ..extensions import db
from ..models import Book
from ..models.audit import AuditLog

books_bp = Blueprint("books", __name__, url_prefix="/books")

def staff_required():
    return current_user.is_authenticated and current_user.role in {"admin", "librarian"}

@books_bp.get("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    query = Book.query
    if q:
        term = f"%{q}%"
        query = query.filter(or_(Book.title.ilike(term), Book.author.ilike(term), Book.isbn.ilike(term)))
    if category:
        query = query.filter_by(category=category)

    books = query.order_by(Book.title.asc()).all()
    categories = [r[0] for r in db.session.query(Book.category).distinct().order_by(Book.category).all()]
    return render_template("books/index.html", books=books, categories=categories, q=q, category=category)

@books_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if not staff_required():
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        total = max(1, int(request.form.get("total_copies", 1)))
        book = Book(
            isbn=request.form["isbn"].strip(),
            title=request.form["title"].strip(),
            author=request.form["author"].strip(),
            category=request.form["category"].strip(),
            publisher=request.form.get("publisher", "").strip(),
            publication_year=int(request.form["publication_year"]) if request.form.get("publication_year") else None,
            total_copies=total,
            available_copies=total,
            shelf=request.form.get("shelf", "").strip(),
            description=request.form.get("description", "").strip()
        )
        db.session.add(book)
        db.session.add(AuditLog(actor_id=current_user.id, action="CREATE_BOOK", entity="book", details=f"Created '{book.title}'"))
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("books.index"))
    return render_template("books/form.html", book=None)

@books_bp.post("/<int:book_id>/delete")
@login_required
def delete(book_id):
    if not staff_required():
        return redirect(url_for("dashboard.index"))
    book = db.session.get(Book, book_id)
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for("books.index"))
    if book.total_copies != book.available_copies:
        flash("Cannot delete a book while copies are on loan.", "warning")
        return redirect(url_for("books.index"))
    db.session.delete(book)
    db.session.commit()
    flash("Book removed.", "success")
    return redirect(url_for("books.index"))
