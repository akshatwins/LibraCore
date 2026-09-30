from datetime import date
from sqlalchemy import func
from ..models import Book, User, Circulation

def metrics():
    total_books = Book.query.count()
    total_copies = int(Book.query.with_entities(func.coalesce(func.sum(Book.total_copies), 0)).scalar() or 0)
    available_copies = int(Book.query.with_entities(func.coalesce(func.sum(Book.available_copies), 0)).scalar() or 0)
    active_members = User.query.filter(User.role == "member", User.is_active_user.is_(True)).count()
    active_loans = Circulation.query.filter_by(returned_at=None).count()
    overdue_loans = Circulation.query.filter(
        Circulation.returned_at.is_(None),
        Circulation.due_date < date.today()
    ).count()

    return {
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "active_members": active_members,
        "active_loans": active_loans,
        "overdue_loans": overdue_loans,
    }
