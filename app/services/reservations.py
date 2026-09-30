from datetime import datetime
from ..extensions import db
from ..models import Book, User, Reservation, Notification

class ReservationError(ValueError):
    pass

def reserve_book(book_id, member_id):
    book = db.session.get(Book, book_id)
    member = db.session.get(User, member_id)
    if not book or not member:
        raise ReservationError("Book or member not found.")

    active = Reservation.query.filter_by(book_id=book.id, member_id=member.id, status="pending").first()
    if active:
        raise ReservationError("You already have an active reservation for this book.")

    reservation = Reservation(book=book, member=member)
    db.session.add(reservation)
    db.session.add(Notification(
        user_id=member.id,
        title="Reservation placed",
        message=f"Your reservation for '{book.title}' has been placed.",
        type="success"
    ))
    db.session.commit()
    return reservation

def cancel_reservation(reservation_id, member_id):
    reservation = db.session.get(Reservation, reservation_id)
    if not reservation or reservation.member_id != member_id:
        raise ReservationError("Reservation not found.")
    reservation.status = "cancelled"
    db.session.commit()
    return reservation
