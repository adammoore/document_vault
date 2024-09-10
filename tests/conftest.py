"""
Pytest configuration file for Document Vault tests.

This module contains fixtures and configuration for the test suite.

Author: Adam Vials Moore
License: Apache 2.0
"""

import pytest
from app import create_app, db, init_scheduler
from app.models import User
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        init_scheduler(app)
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class MockOAuthClient:
    def prepare_request_uri(self, *args, **kwargs):
        return "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=mock-client-id&redirect_uri=mock-redirect-uri"
class AuthActions:
    """Helper class for authentication actions in tests."""

    def __init__(self, client):
        self._client = client

    def login(self, email='test@example.com', name='Test User'):
        """Log in as a test user."""
        with app.app_context():
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, name=name)
                db.session.add(user)
                db.session.commit()
        return self._client.get('/login')

    def logout(self):
        """Log out the current user."""
        return self._client.get('/logout')

@pytest.fixture
def auth(client):
    """Authentication actions for tests."""
    return AuthActions(client)

@pytest.fixture(autouse=True)
def db_session(app):
    """Create a new database session for a test."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        db.session = session
        yield session
        transaction.rollback()
        connection.close()
        session.remove()