from iThACK.database.database import Database
from iThACK.manage import select_account, add_account, view_password, delete_account, check_breach
from iThACK.security import login
from iThACK.ui import set_mode, tabulate

mp_hash = login()


def process(argv, argc):
    if argc == 0:
        set_mode("View Mode")
        tabulate(Database().read(accounts=True))

        while True:
            _id = select_account()
            view_password(_id, mp_hash)

    elif argv[0] == "add":
        set_mode("Add Mode")
        add_account(mp_hash)

    elif argv[0] == "view":
        set_mode("View Mode")
        tabulate(Database().read(accounts=True))

        while True:
            _id = select_account()
            view_password(_id, mp_hash)

    elif argv[0] == "remove":
        set_mode("Remove Mode")
        tabulate(Database().read(accounts=True))

        while True:
            _id = select_account()
            delete_account(_id)

    elif argv[0] == "pwned":
        set_mode("Pwned Mode")
        check_breach(mp_hash)
