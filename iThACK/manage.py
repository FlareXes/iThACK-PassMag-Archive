import sys

from iThACK.database.database import Database, Filter
from iThACK.security import encrypt_password, AES256
from iThACK.template import Account
from iThACK.ui import tabulate, Print, Input


def select_account():
    tabulate(Database().read)

    while True:
        _id = Input.prompt()
        if _id.isdigit():
            return int(_id)
        elif _id == "q" or _id == "quit" or _id == "exit":
            sys.exit(0)
        else:
            Print.fail("[  Invalid Option  ]\n")


def add_account(mp_hash: bytes):
    site = input("Site: ")
    username = input("Username / E-Mail: ")
    creds = encrypt_password(mp_hash)
    url = input("URL: ")

    account = Account(0, site, username, url)
    Database(account, creds).create()
    Print.success(":) Added new account")


def delete_account(_id):
    account, cc = Filter().select(_id)

    if Input.confirm():
        Database(account=account).delete()
        Print.fail("[-] Account Removed")


def view_password(_id, mp_hash):
    account, cc = Filter().select(_id)
    aes = AES256(mp_hash)
    print(aes.decrypt(cc))
