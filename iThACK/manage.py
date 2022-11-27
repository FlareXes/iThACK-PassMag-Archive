from iThACK.database.database import Database, Filter
from iThACK.template import Account
from iThACK.ui.ui import tabulate


def select_account():
    tabulate(Database().read)
    _id = int(input(": "))
    account = Filter().select(_id)
    return account


def add_account():
    site = input("Site: ")
    username = input("Username / E-Mail: ")
    password = input("Password: ")
    url = input("URL: ")

    acc = Account(0, site, username, url)
    Database(acc).create()


def delete_account():
    account = select_account()
    Database(account).delete()
