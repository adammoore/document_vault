# Document Vault

Document Vault is a secure document storage system with time-based messaging functionality. It allows users to store documents, manage recipients, and send automatic notifications based on configurable timers.

## Features

- Secure document storage and management
- Recipient management
- Time-based messaging system
- User authentication via Google OAuth
- Configuration management for SMTP and other parameters
- Web interface for easy management

## Project Structure

```
document_vault/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── tasks.py
│   ├── email.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── documents.py
│   │   ├── recipients.py
│   │   └── main.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── config.html
│       ├── recipients.html
│       ├── add_recipient.html
│       ├── edit_recipient.html
│       ├── documents.html
│       ├── add_document.html
│       ├── edit_document.html
│       ├── reset_password_request.html
│       ├── reset_password.html
│       └── 404.html
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_config.py
│   ├── test_documents.py
│   └── test_recipients.py
│
├── migrations/
│
├── config.py
├── requirements.txt
├── run.py
├── .env
├── .gitignore
├── run_celery.sh
├── README.md
└── Updates.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/document_vault.git
   cd document_vault
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the `.env` file with your configuration (see `.env.example` for required variables).

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

7. In a separate terminal, run the Celery worker:
   ```
   ./run_celery.sh
   ```

## Testing

To run the tests:
```
flask test
```

## License

This project is licensed under the Apache 2.0 License.

## Author

Adam Vials Moore