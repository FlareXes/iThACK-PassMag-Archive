import os
from platform import system

USER_HOME_DIR = os.path.expanduser("~")

if system() == "Windows":
    DATABASE_DIR = os.path.join(os.getenv("APPDATA"), "iThACK")
elif system() == "Darwin":
    DATABASE_DIR = os.path.join(USER_HOME_DIR, "Library", "Application Support" "iThACK")
else:
    DATABASE_DIR = os.path.join(USER_HOME_DIR, ".local", "share", "iThACK")

DATABASE = os.path.join(DATABASE_DIR, "accounts.db")

os.makedirs(DATABASE_DIR, exist_ok=True)
