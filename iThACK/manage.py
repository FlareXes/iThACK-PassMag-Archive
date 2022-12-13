from iThACK.database.database import Database, Filter
from iThACK.security import encrypt_password
from iThACK.template import Account
from iThACK.ui import tabulate


def select_account():
    tabulate(Database().read)
    _id = int(input(": "))
    account = Filter().select(_id)
    return account


def add_account(mp_hash: bytes):
    site = input("Site: ")
    username = input("Username / E-Mail: ")
    creds = encrypt_password(mp_hash)
    url = input("URL: ")

    account = Account(0, site, username, url)
    Database(account, creds).create()
