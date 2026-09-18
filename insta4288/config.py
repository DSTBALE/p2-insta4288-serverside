"""Configure the Insta4288 development application."""
import pathlib

APPLICATION_ROOT = '/'
SESSION_COOKIE_NAME = 'login'
INSTA4288_ROOT = pathlib.Path(__file__).resolve().parent.parent
SECRET_KEY = (INSTA4288_ROOT / 'var' / 'secret_key').read_bytes()
UPLOAD_FOLDER = INSTA4288_ROOT / 'var' / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DATABASE_FILENAME = INSTA4288_ROOT / 'var' / 'insta4288.sqlite3'
