import pytest

from models import app, db


@pytest.fixture
def db_session():
    """Base SQLite en mémoire, isolée pour chaque test."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.engine.dispose()
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
