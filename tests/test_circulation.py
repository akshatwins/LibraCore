from datetime import date, timedelta
from app.extensions import db
from app.models import User, Book, Circulation
from app.services.circulation import issue_book, return_book

def setup_entities(app):
    with app.app_context():
        admin = User(name="Admin", email="a@x.com", role="admin")
        admin.set_password("Password123")
        member = User(name="Member", email="m@x.com", role="member")
        member.set_password("Password123")
        book = Book(isbn="123", title="Testing", author="Tester", category="Testing", total_copies=2, available_copies=2)
        db.session.add_all([admin, member, book])
        db.session.commit()
        return admin.id, member.id, book.id

def test_issue_decreases_inventory(app):
    admin_id, member_id, book_id = setup_entities(app)
    with app.app_context():
        loan = issue_book(book_id, member_id, admin_id)
        assert loan.id is not None
        assert db.session.get(Book, book_id).available_copies == 1

def test_return_restores_inventory(app):
    admin_id, member_id, book_id = setup_entities(app)
    with app.app_context():
        loan = issue_book(book_id, member_id, admin_id)
        return_book(loan.id, admin_id)
        assert db.session.get(Book, book_id).available_copies == 2
