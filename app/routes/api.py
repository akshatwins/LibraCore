from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Book, User, Circulation

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/books")
@login_required
def books():
    items = Book.query.order_by(Book.title).all()
    return jsonify({
        "data": [{
            "id": b.id,
            "isbn": b.isbn,
            "title": b.title,
            "author": b.author,
            "category": b.category,
            "total_copies": b.total_copies,
            "available_copies": b.available_copies
        } for b in items]
    })

@api_bp.get("/members")
@login_required
def members():
    items = User.query.filter_by(role="member").order_by(User.name).all()
    return jsonify({"data": [{"id": u.id, "name": u.name, "email": u.email} for u in items]})

@api_bp.get("/circulation")
@login_required
def circulation():
    items = Circulation.query.order_by(Circulation.issued_at.desc()).limit(100).all()
    return jsonify({"data": [{
        "id": x.id,
        "book": x.book.title,
        "member": x.member.name,
        "issued_at": x.issued_at.isoformat(),
        "due_date": x.due_date.isoformat(),
        "returned_at": x.returned_at.isoformat() if x.returned_at else None,
        "status": x.status,
        "fine_amount": x.fine_amount
    } for x in items]})

@api_bp.post("/books")
@login_required
def create_book():
    if current_user.role not in {"admin", "librarian"}:
        return jsonify({"error": "Forbidden"}), 403
    payload = request.get_json(silent=True) or {}
    required = ["isbn", "title", "author", "category"]
    if any(not payload.get(k) for k in required):
        return jsonify({"error": "isbn, title, author and category are required"}), 400

    total = max(1, int(payload.get("total_copies", 1)))
    book = Book(
        isbn=payload["isbn"],
        title=payload["title"],
        author=payload["author"],
        category=payload["category"],
        total_copies=total,
        available_copies=total
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "message": "Book created"}), 201

@api_bp.post("/members")
@login_required
def create_member():
    if current_user.role not in {"admin", "librarian"}:
        return jsonify({"error": "Forbidden"}), 403
    payload = request.get_json(silent=True) or {}
    if not payload.get("name") or not payload.get("email") or not payload.get("password"):
        return jsonify({"error": "name, email and password are required"}), 400
    if User.query.filter_by(email=payload["email"].lower()).first():
        return jsonify({"error": "Email already exists"}), 409

    member = User(name=payload["name"], email=payload["email"].lower(), role="member")
    member.set_password(payload["password"])
    db.session.add(member)
    db.session.commit()
    return jsonify({"id": member.id, "message": "Member created"}), 201


@api_bp.get("/reservations")
@login_required
def reservations():
    from ..models import Reservation
    items = Reservation.query.order_by(Reservation.reserved_at.desc()).limit(100).all()
    return jsonify({"data": [{
        "id": r.id,
        "book": r.book.title,
        "member": r.member.name,
        "status": r.status,
        "reserved_at": r.reserved_at.isoformat()
    } for r in items]})

@api_bp.get("/analytics")
@login_required
def analytics_data():
    from ..services.analytics import analytics
    return jsonify(analytics())
