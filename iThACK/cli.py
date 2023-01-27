from iThACK.manage import select_account, add_account, view_password, delete_account, check_breach
from iThACK.security import login

mp_hash = login()


def process(argv, argc):
    if argc == 0:
        _id = select_account()
        view_password(_id, mp_hash)

    elif argv[0] == "add":
        add_account(mp_hash)

    elif argv[0] == "view":
        _id = select_account()
        view_password(_id, mp_hash)

    elif argv[0] == "remove":
        _id = select_account()
        delete_account(_id)

    elif argv[0] == "pwned":
        check_breach(mp_hash)
