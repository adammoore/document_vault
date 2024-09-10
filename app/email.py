"""
Email utilities for Document Vault

This module contains functions for sending emails in the Document Vault application.

Author: Adam Vials Moore
License: Apache 2.0
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, url_for


def send_reset_email(user, token):
    """
    Send a reset email to the user with a reset link.

    :param user: The user object
    :param token: The reset token
    """
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    msg = MIMEMultipart()
    msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = user.email
    msg['Subject'] = "Reset Your Password"

    body = f"""
    Hello {user.name},

    To reset your password, please click on the following link:

    {reset_link}

    If you did not request a password reset, please ignore this email.

    Best regards,
    The Document Vault Team
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.send_message(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False


def send_email(config, to_email, subject, body):
    """
    Send an email using the provided configuration.

    :param config: The application configuration containing SMTP settings
    :param to_email: The recipient's email address
    :param subject: The subject of the email
    :param body: The body content of the email
    :return: Boolean indicating whether the email was sent successfully
    """
    msg = MIMEMultipart()
    msg['From'] = config.smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            server.starttls()
            server.login(config.smtp_username, config.smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False


def send_test_email(config):
    """
    Send a test email using the provided configuration.

    :param config: The application configuration containing SMTP settings
    :return: Boolean indicating whether the test email was sent successfully
    """
    subject = "Test Email from Document Vault"
    body = "This is a test email from your Document Vault application. If you received this, your SMTP configuration is working correctly."

    return send_email(config, config.smtp_username, subject, body)