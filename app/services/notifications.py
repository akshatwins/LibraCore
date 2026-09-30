from datetime import date, timedelta
from ..extensions import db
from ..models import Circulation, Notification

def generate_due_notifications():
    today = date.today()
    created = 0
    loans = Circulation.query.filter(Circulation.returned_at.is_(None)).all()

    for loan in loans:
        days = (loan.due_date - today).days
        if days in {3, 1, 0}:
            label = "today" if days == 0 else f"in {days} day(s)"
            exists = Notification.query.filter(
                Notification.user_id == loan.member_id,
                Notification.title == "Book due reminder",
                Notification.message.ilike(f"%{loan.book.title}%"),
                Notification.created_at >= today
            ).first()
            if not exists:
                db.session.add(Notification(
                    user_id=loan.member_id,
                    title="Book due reminder",
                    message=f"'{loan.book.title}' is due {label}.",
                    type="warning"
                ))
                created += 1

        if days < 0:
            exists = Notification.query.filter(
                Notification.user_id == loan.member_id,
                Notification.title == "Overdue book",
                Notification.message.ilike(f"%{loan.book.title}%"),
                Notification.created_at >= today
            ).first()
            if not exists:
                db.session.add(Notification(
                    user_id=loan.member_id,
                    title="Overdue book",
                    message=f"'{loan.book.title}' is {abs(days)} day(s) overdue.",
                    type="danger"
                ))
                created += 1

    db.session.commit()
    return created
