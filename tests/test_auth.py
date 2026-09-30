from app.extensions import db
from app.models import User

def test_login(client, app):
    with app.app_context():
        u = User(name="Test Admin", email="test@example.com", role="admin")
        u.set_password("Password123")
        db.session.add(u)
        db.session.commit()

    response = client.post("/login", data={"email":"test@example.com","password":"Password123"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data
