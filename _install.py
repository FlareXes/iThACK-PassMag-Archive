from User._user_db import create_database
from User._master_encryption import passwordHasher

if __name__ == '__main__':
    create_database()
    passwordHasher("don't use weak master password")