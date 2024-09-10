"""
Pytest configuration file for Document Vault tests.

This module contains fixtures and configuration for the test suite.

Author: Adam Vials Moore
License: Apache 2.0
"""

import pytest
from app import create_app, db, scheduler
from app.models import User
from config import TestConfig
from unittest.mock import Mock

class MockOAuthClient:
    def prepare_request_uri(self, *args, **kwargs):
        return "http://mock-auth-url"

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    app.oauth_client = MockOAuthClient()  # Use mock OAuth client for tests

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    # Stop the scheduler after tests
    scheduler.shutdown()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class AuthActions:
    """Helper class for authentication actions in tests."""

    def __init__(self, client):
        self._client = client

    def login(self, email='test@example.com', name='Test User'):
        """Log in as a test user."""
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