"""
WSGI entry point for Document Vault application.

This module creates and configures the Flask application instance.

Author: Adam Vials Moore
License: Apache 2.0
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()