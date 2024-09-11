import click
from flask.cli import with_appcontext
from app import db
from app.models import Document
from app.tasks import check_document_expiry
from datetime import datetime, timedelta

@click.command('check-expiry')
@with_appcontext
def check_expiry_command():
    """Manually trigger document expiry check."""
    result = check_document_expiry()
    click.echo(result)

@click.command('set-test-expiry')
@click.argument('document_id', type=int)
@click.argument('minutes', type=int)
@with_appcontext
def set_test_expiry_command(document_id, minutes):
    """Set a test expiry time for a document."""
    document = Document.query.get(document_id)
    if document:
        document.updated_at = datetime.utcnow() - timedelta(minutes=minutes)
        db.session.commit()
        click.echo(f"Document {document_id} expiry set to {minutes} minutes ago.")
    else:
        click.echo(f"Document {document_id} not found.")

def init_app(app):
    app.cli.add_command(check_expiry_command)
    app.cli.add_command(set_test_expiry_command)