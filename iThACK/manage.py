from iThACK.database.database import Database, Filter
from iThACK.security import getpass
from iThACK.security.utils import get_mp_hash
from iThACK.template import Account
from iThACK.ui.ui import tabulate


def select_account():
    tabulate(Database().read)
    _id = int(input(": "))
    account = Filter().select(_id)
    return account


def add_account():
    mp_hash = get_mp_hash()
    site = input("Site: ")
    username = input("Username / E-Mail: ")
    creds = getpass(mp_hash)
    url = input("URL: ")

    account = Account(0, site, username, url)
    Database(account, creds).create()
