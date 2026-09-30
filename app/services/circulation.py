from datetime import date, timedelta, datetime
from flask import current_app
from ..extensions import db
from ..models import Book, User, Circulation, AuditLog

class CirculationError(ValueError):
    pass

def issue_book(book_id, member_id, actor_id):
    book = db.session.get(Book, book_id)
    member = db.session.get(User, member_id)

    if not book:
        raise CirculationError("Book not found.")
    if not member or member.role not in {"member", "librarian", "admin"}:
        raise CirculationError("Member not found or inactive.")
    if book.available_copies <= 0:
        raise CirculationError("No copies of this book are currently available.")

    active = Circulation.query.filter_by(book_id=book.id, member_id=member.id, returned_at=None).first()
    if active:
        raise CirculationError("This member already has an active loan for this book.")

    loan = Circulation(
        book=book,
        member=member,
        due_date=date.today() + timedelta(days=current_app.config["LOAN_PERIOD_DAYS"])
    )
    book.available_copies -= 1

    db.session.add(loan)
    db.session.add(AuditLog(
        actor_id=actor_id,
        action="ISSUE_BOOK",
        entity="circulation",
        details=f"Issued '{book.title}' to {member.name}"
    ))
    db.session.commit()
    return loan

def return_book(loan_id, actor_id):
    loan = db.session.get(Circulation, loan_id)
    if not loan:
        raise CirculationError("Loan not found.")
    if loan.returned_at:
        raise CirculationError("This loan has already been returned.")

    loan.returned_at = datetime.utcnow()
    loan.fine_amount = loan.days_overdue * current_app.config["FINE_PER_DAY"]
    loan.book.available_copies = min(loan.book.available_copies + 1, loan.book.total_copies)

    db.session.add(AuditLog(
        actor_id=actor_id,
        action="RETURN_BOOK",
        entity="circulation",
        entity_id=loan.id,
        details=f"Returned '{loan.book.title}' with fine ₹{loan.fine_amount:.2f}"
    ))
    db.session.commit()
    return loan

def renew_book(loan_id, actor_id):
    loan = db.session.get(Circulation, loan_id)
    if not loan or loan.returned_at:
        raise CirculationError("Active loan not found.")
    if loan.renewal_count >= 2:
        raise CirculationError("Maximum renewals reached.")

    loan.due_date += timedelta(days=current_app.config["LOAN_PERIOD_DAYS"])
    loan.renewal_count += 1
    db.session.add(AuditLog(
        actor_id=actor_id,
        action="RENEW_BOOK",
        entity="circulation",
        entity_id=loan.id,
        details=f"Renewed '{loan.book.title}'"
    ))
    db.session.commit()
    return loan
