"""Shiba_inc development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'$(python3 -c "import os; print(os.urandom(24))")'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SHIBA_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SHIBA_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SHIBA_ROOT/'var'/'shiba_inc.sqlite3'
