#!/bin/bash

# Setup script for Document Vault Project
# Author: Adam Vials Moore
# License: Apache 2.0

# Create project directory
mkdir -p document_vault
cd document_vault

# Create main Python file
cat > document_vault.py << EOL
"""
Document Vault with Time-Based Messaging

This script implements a document vault system with a time-based messaging feature.
It includes functionality to store documents, reset a countdown timer via email link,
and send notifications if the timer expires.

Author: Adam Vials Moore
License: Apache 2.0
"""

# Paste the content of the document_vault.py file here
EOL

# Create requirements file
cat > requirements.txt << EOL
Flask==2.0.1
EOL

# Create README file
cat > README.md << EOL
# Document Vault

A secure document storage system with time-based messaging functionality.

## Features
- Store and retrieve documents
- Reset countdown timer via email link
- Automatic message sending when countdown expires

## Setup
1. Clone the repository
2. Install dependencies: \`pip install -r requirements.txt\`
3. Run the application: \`python document_vault.py\`

## License
Apache 2.0

## Author
Adam Vials Moore
EOL

# Create .gitignore file
cat > .gitignore << EOL
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.log
EOL

# Initialize git repository
git init

# Create initial commit
git add .
git commit -m "Initial commit: Set up Document Vault project structure"

echo "Project structure set up successfully!"
echo "Next steps:"
echo "1. Review and update the document_vault.py file with the full implementation"
echo "2. Create a new repository on GitHub"
echo "3. Link your local repository to the GitHub repository:"
echo "   git remote add origin https://github.com/yourusername/document-vault.git"
echo "4. Push your code to GitHub:"
echo "   git push -u origin main"
EOL

chmod +x setup_project.sh