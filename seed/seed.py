from datetime import date, timedelta
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import User, Book, Circulation

app = create_app()

BOOKS = [
    ("9780132350884","Clean Code","Robert C. Martin","Software Engineering","Prentice Hall",2008,4,"A-01"),
    ("9780134685991","Effective Java","Joshua Bloch","Programming","Addison-Wesley",2018,3,"A-02"),
    ("9781492051367","Designing Data-Intensive Applications","Martin Kleppmann","Data Engineering","O'Reilly",2017,3,"B-01"),
    ("9781098104030","Fluent Python","Luciano Ramalho","Python","O'Reilly",2022,2,"A-03"),
    ("9780131103627","The C Programming Language","Brian W. Kernighan","Programming","Prentice Hall",1988,3,"C-01"),
    ("9780262046305","Introduction to Algorithms","Thomas H. Cormen","Algorithms","MIT Press",2022,2,"C-02"),
    ("9780135974445","Database System Concepts","Abraham Silberschatz","Databases","McGraw Hill",2020,3,"B-02"),
    ("9781119454148","Python for Data Analysis","Wes McKinney","Data Science","O'Reilly",2022,3,"B-03"),
    ("9781491957660","Hands-On Machine Learning","Aurélien Géron","Machine Learning","O'Reilly",2022,2,"B-04"),
    ("9781617294433","The Well-Grounded Java Developer","Benjamin J. Evans","Java","Manning",2022,2,"A-04"),
]

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(name="System Administrator", email="admin@library.local", role="admin")
    admin.set_password("Admin@123")
    librarian = User(name="Main Librarian", email="librarian@library.local", role="librarian")
    librarian.set_password("Librarian@123")
    members = []
    for i in range(1, 8):
        m = User(name=f"Demo Member {i}", email=f"member{i}@library.local", role="member")
        m.set_password("Member@123")
        members.append(m)

    db.session.add_all([admin, librarian, *members])

    books = []
    for row in BOOKS:
        isbn,title,author,category,publisher,year,copies,shelf = row
        books.append(Book(isbn=isbn,title=title,author=author,category=category,publisher=publisher,publication_year=year,total_copies=copies,available_copies=copies,shelf=shelf,language='English',pages=300))
    db.session.add_all(books)
    db.session.commit()

    # Demo active and overdue loans
    loan1 = Circulation(book=books[0], member=members[0], due_date=date.today()+timedelta(days=8))
    books[0].available_copies -= 1
    loan2 = Circulation(book=books[2], member=members[1], due_date=date.today()-timedelta(days=4))
    books[2].available_copies -= 1
    loan3 = Circulation(book=books[4], member=members[2], due_date=date.today()+timedelta(days=3))
    books[4].available_copies -= 1

    db.session.add_all([loan1,loan2,loan3])
    db.session.commit()

    print("Seed complete.")
    print("Admin: admin@library.local / Admin@123")
    print("Librarian: librarian@library.local / Librarian@123")
    print("Members: member1@library.local ... member7@library.local / Member@123")
