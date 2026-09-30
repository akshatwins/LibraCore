from datetime import date, timedelta
from sqlalchemy import func
from ..models import Book, User, Circulation, Reservation

def analytics():
    today = date.today()
    last_30 = today - timedelta(days=30)

    popular = (
        Circulation.query
        .join(Book)
        .with_entities(Book.title, func.count(Circulation.id).label("count"))
        .group_by(Book.id)
        .order_by(func.count(Circulation.id).desc())
        .limit(8).all()
    )

    categories = (
        Circulation.query
        .join(Book)
        .with_entities(Book.category, func.count(Circulation.id).label("count"))
        .filter(Circulation.issued_at >= last_30)
        .group_by(Book.category)
        .order_by(func.count(Circulation.id).desc()).all()
    )

    return {
        "popular_books": [{"label": x[0], "value": x[1]} for x in popular],
        "categories": [{"label": x[0], "value": x[1]} for x in categories],
        "reservations": Reservation.query.filter_by(status="pending").count(),
        "new_members_30d": User.query.filter(User.created_at >= last_30, User.role == "member").count(),
    }
