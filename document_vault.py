import os
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

class DocumentVault:
    def __init__(self, countdown_duration=7*24*60*60):  # Default 7 days
        self.documents = {}
        self.last_alive_signal = datetime.now()
        self.countdown_duration = countdown_duration
        self.message_sent = False

    def add_document(self, doc_id, content):
        """Add a document to the vault."""
        self.documents[doc_id] = content

    def get_document(self, doc_id):
        """Retrieve a document from the vault."""
        return self.documents.get(doc_id)

    def reset_countdown(self):
        """Reset the countdown timer."""
        self.last_alive_signal = datetime.now()
        self.message_sent = False

    def check_and_send_message(self):
        """Check if it's time to send the message and send if necessary."""
        if not self.message_sent and (datetime.now() - self.last_alive_signal).total_seconds() > self.countdown_duration:
            self.send_message()
            self.message_sent = True

    def send_message(self):
        """Send the message with document information."""
        subject = "Document Vault: No Activity Alert"
        body = "No 'I'm alive' signal received in the specified time. Here are the stored documents:\n\n"
        for doc_id, content in self.documents.items():
            body += f"Document ID: {doc_id}\nContent: {content}\n\n"

        # Email sending logic (replace with your SMTP settings)
        sender_email = "your_email@example.com"
        receiver_email = "receiver@example.com"
        password = "your_password"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

vault = DocumentVault()

@app.route('/alive', methods=['GET'])
def alive_signal():
    """Endpoint to receive the 'I'm alive' signal."""
    vault.reset_countdown()
    return jsonify({"status": "Countdown reset successfully"}), 200

@app.route('/document', methods=['POST'])
def add_document():
    """Endpoint to add a document to the vault."""
    data = request.json
    doc_id = data.get('id')
    content = data.get('content')
    if doc_id and content:
        vault.add_document(doc_id, content)
        return jsonify({"status": "Document added successfully"}), 201
    return jsonify({"error": "Invalid document data"}), 400

if __name__ == '__main__':
    app.run(debug=True)

# Run this in a separate thread or process
while True:
    vault.check_and_send_message()
    time.sleep(60)  # Check every minute