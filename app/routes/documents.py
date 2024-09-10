"""
Document Management Routes for Document Vault

This module contains routes for managing documents.

Author: Adam Vials Moore
License: Apache 2.0
"""

import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Document, Recipient
from app import db

bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/documents')
@login_required
def list_documents():
    documents = Document.query.filter_by(user_id=current_user.id).options(db.joinedload(Document.recipient)).all()
    return render_template('documents.html', documents=documents)


@bp.route('/documents/add', methods=['GET', 'POST'])
@login_required
def add_document():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        recipient_id = request.form.get('recipient_id')
        scheduled_send = request.form.get('scheduled_send')
        file = request.files.get('file')

        document = Document(title=title, content=content, user_id=current_user.id)

        if recipient_id:
            document.recipient_id = recipient_id

        if scheduled_send:
            document.scheduled_send = datetime.fromisoformat(scheduled_send)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            document.file_path = file_path

        db.session.add(document)
        db.session.commit()
        flash('Document added successfully', 'success')
        return redirect(url_for('documents.list_documents'))

    recipients = Recipient.query.all()
    return render_template('add_document.html', recipients=recipients)

@bp.route('/documents/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_document(id):
    document = Document.query.get_or_404(id)
    if document.user_id != current_user.id:
        flash('You do not have permission to edit this document', 'danger')
        return redirect(url_for('documents.list_documents'))

    if request.method == 'POST':
        document.title = request.form['title']
        document.content = request.form['content']
        document.recipient_id = request.form.get('recipient_id')
        scheduled_send = request.form.get('scheduled_send')

        if scheduled_send:
            document.scheduled_send = datetime.fromisoformat(scheduled_send)

        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            document.file_path = file_path

        db.session.commit()
        flash('Document updated successfully', 'success')
        return redirect(url_for('documents.list_documents'))

    recipients = Recipient.query.all()
    return render_template('edit_document.html', document=document, recipients=recipients)

@bp.route('/documents/delete/<int:id>')
@login_required
def delete_document(id):
    document = Document.query.get_or_404(id)
    if document.user_id != current_user.id:
        flash('You do not have permission to delete this document', 'danger')
        return redirect(url_for('documents.list_documents'))

    if document.file_path:
        try:
            os.remove(document.file_path)
        except OSError:
            flash('Error: File could not be deleted', 'danger')

    db.session.delete(document)
    db.session.commit()
    flash('Document deleted successfully', 'success')
    return redirect(url_for('documents.list_documents'))