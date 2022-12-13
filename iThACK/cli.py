import sys

from iThACK.manage import select_account, add_account
from iThACK.security import login
from iThACK.ui import Print

mp_hash = login()


def process(argv, argc):
    if argc == 0:
        select_account()

    if argv[0] == "add":
        add_account(mp_hash)
        Print.success(":) Added new account")
