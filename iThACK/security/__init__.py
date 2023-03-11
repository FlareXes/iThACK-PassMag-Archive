import sys

from Cryptodome.Hash.SHA1 import SHA1Hash

from iThACK.database.database import Filter, Database
from iThACK.security.AES import AES256
from iThACK.security.HIBP import have_i_been_pwned
from iThACK.security.master_password import MasterPassword
from iThACK.ui import Print


def encrypt_password(mp_hash: bytes):
    password = input("Password: ")
    aes = AES256(mp_hash)
    cc = aes.encrypt(password)
    return cc


def login():
    mp = MasterPassword()
    for _ in range(3):
        trust = mp.authenticate()
        if trust:
            return mp.mp_hash
   
    Print.fail(">>>  Failed: Too many invalid attempts  <<<")
    sys.exit(1)


def pwned_accounts(mp_hash: bytes):
    breached = []
    account_ids = Database().read("id")
    for i, _id in enumerate(account_ids):
        print(f"{len(breached)}/{i + 1} : Passwords Have Been Pwned", end="\r")
        account, cc = Filter().select(_id[0])
        password_hash = SHA1Hash(AES256(mp_hash).decrypt(cc).encode("utf-8")).hexdigest()
        pwned = have_i_been_pwned(password_hash)
        if pwned:
            breached.append(account)

    Print.warning(f"{len(breached)}/{len(account_ids)} : Passwords Have Been Pwned")
    return breached
