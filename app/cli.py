"""
CLI commands for Document Vault

This module contains custom CLI commands for the Document Vault application.

Author: Adam Vials Moore
License: Apache 2.0
"""

import click
from flask.cli import with_appcontext
from datetime import datetime, timedelta

def init_app(app):
    @app.cli.command('check-expiry')
    @with_appcontext
    def check_expiry_command():
        """Manually trigger document expiry check."""
        from app.tasks import check_document_expiry
        result = check_document_expiry()
        click.echo(result)

    @app.cli.command('set-test-expiry')
    @click.argument('document_id', type=int)
    @click.argument('minutes', type=int)
    @with_appcontext
    def set_test_expiry_command(document_id, minutes):
        """Set a test expiry time for a document."""
        from app.models import Document
        from app import db
        document = Document.query.get(document_id)
        if document:
            document.updated_at = datetime.utcnow() - timedelta(minutes=minutes)
            db.session.commit()
            click.echo(f"Document {document_id} expiry set to {minutes} minutes ago.")
        else:
            click.echo(f"Document {document_id} not found.")