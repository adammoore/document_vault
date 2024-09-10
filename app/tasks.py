"""
Background Tasks for Document Vault

This module contains background tasks for the Document Vault application.

Author: Adam Vials Moore
License: Apache 2.0
"""

from app import db
from app.models import Document
from datetime import datetime, timedelta
from flask import current_app

def check_document_expiry():
    """
    Check for expired documents and handle notifications.

    This function queries the database for documents that have not been
    updated in the last 7 days and simulates sending notifications.
    """
    with current_app.app_context():
        expiry_threshold = datetime.utcnow() - timedelta(days=7)
        expired_documents = Document.query.filter(
            Document.updated_at < expiry_threshold
        ).all()

        for document in expired_documents:
            # TODO: Implement actual notification logic
            print(f"Document {document.id} has expired. Notification should be sent.")

        return f"Checked {len(expired_documents)} expired documents."