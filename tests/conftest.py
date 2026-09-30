import pytest
from app import create_app
from app.config import Config
from app.extensions import db

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
