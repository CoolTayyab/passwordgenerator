# Password Manager

A desktop password manager built with Python and CustomTkinter. The application provides secure password generation, encrypted local data storage, password history, master-password protection, and Google authentication/backup support.

## Features

- Secure password generator
- Custom password options
- Copy generated passwords to clipboard
- Show/hide password functionality
- Password history
- Master password protection
- Fernet-based encryption
- Google OAuth authentication
- Firebase/Google Drive integration support
- Desktop GUI built with CustomTkinter

## Technologies

- Python
- CustomTkinter
- Cryptography (Fernet)
- bcrypt
- Pillow
- Google OAuth / Google APIs
- Firebase integration
- Pyperclip

## Project Structure

```text
passwordgenerator/
├── app.py
├── auth.py
├── config.py
├── database.py
├── encryption.py
├── history.py
├── login.py
├── main.py
├── master_password.py
├── ui.py
├── utils.py
├── test_firebase.py
├── requirements.txt
├── assets/
└── data/
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CoolTayyab/password-generator.git
cd password-generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Security

Sensitive files and local user data should never be committed to GitHub. This project uses a `.gitignore` file to exclude local credentials, OAuth tokens, encryption keys, password hashes, password history, virtual environments, and other private files.

Do not upload files such as:

```text
data/token.json
data/secret.key
data/firebase_key.json
data/master.hash
data/history.json
assets/client_secret.json
```

## Important Note

This project is intended for educational and personal use. Always protect your master password and keep authentication credentials and encryption keys private.

## Future Improvements

- Password strength meter
- Search and filtering for saved passwords
- Password categories
- Automatic encrypted backups
- Improved account recovery
- Packaged desktop executable
- Additional security and audit features

## License

This project is currently provided for personal and educational use.
