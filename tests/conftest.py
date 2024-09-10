import pytest
from app import create_app, db
from app.models import User
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    _app = create_app(TestConfig)

    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client, app):
        self._client = client
        self._app = app

    def login(self, email='test@example.com', name='Test User'):
        with self._app.app_context():
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, name=name)
                db.session.add(user)
                db.session.commit()
        return self._client.get('/login')

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client, app):
    return AuthActions(client, app)