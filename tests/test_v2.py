from app.extensions import db
from app.models import User, Book, Reservation
from app.services.reservations import reserve_book

def test_member_can_reserve_book(app):
    with app.app_context():
        member = User(name="Member", email="member@test.com", role="member")
        member.set_password("Password123")
        book = Book(isbn="999", title="Unavailable Book", author="Author", category="Test", total_copies=1, available_copies=0)
        db.session.add_all([member, book])
        db.session.commit()

        reservation = reserve_book(book.id, member.id)
        assert reservation.status == "pending"
        assert Reservation.query.count() == 1
