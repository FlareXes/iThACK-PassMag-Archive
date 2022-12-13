from iThACK.manage import select_account, add_account, view_password, delete_account
from iThACK.security import login
from iThACK.ui import Print

mp_hash = login()


def process(argv, argc):
    if argc == 0:
        select_account()

    if argv[0] == "add":
        add_account(mp_hash)

    elif argv[0] == "view":
        _id = select_account()
        view_password(_id, mp_hash)

    elif argv[0] == "remove":
        _id = select_account()
        delete_account(_id)
