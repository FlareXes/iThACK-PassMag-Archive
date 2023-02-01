import sys
import pyperclip

from iThACK.database.database import Database, Filter
from iThACK.security import encrypt_password, AES256, pwned_accounts
from iThACK.template import Account
from iThACK.ui import tabulate, Print, Input, get_mode
from iThACK.utils import attrs

PROMPT_PASSWORD = False


def select_account():
    while True:
        _id = Input.prompt(f"\n[bold bright_yellow]{get_mode()}[/bold bright_yellow]")
        if _id.isdigit():
            return int(_id)

        elif _id == "p":
            global PROMPT_PASSWORD
            PROMPT_PASSWORD = not PROMPT_PASSWORD

        elif _id == "v":
            tabulate(Database().read(accounts=True))

        elif _id == "q" or _id == "quit" or _id == "exit":
            sys.exit(0)

        else:
            Print.fail("[  Invalid Option  ]")


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
    if PROMPT_PASSWORD:
        Print.fail(aes.decrypt(cc))
        pyperclip.copy(aes.decrypt(cc))
    else:
        pyperclip.copy(aes.decrypt(cc))
        Print.success("Copied To Clipboard !!")


def check_breach(mp_hash):
    pwned = pwned_accounts(mp_hash)
    if len(pwned) > 0:
        pwned_list = list(map(lambda account: attrs(account), pwned))
        tabulate(pwned_list)
        Print.fail(":( You Are Not Safe, These Accounts' Passwords Have Been Breached")
        Print.fail("\tIf you've ever used it anywhere before, change it!")
    else:
        Print.success(":) You're Safe, Passwords Haven't Been Breached")
