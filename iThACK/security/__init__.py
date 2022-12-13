import sys

from iThACK.security.AES import AES256
from iThACK.security.master_password import MasterPassword
from iThACK.ui import Print


def encrypt_password(mp_hash: bytes):
    password = input("Password: ")
    aes = AES256(mp_hash)
    cc = aes.encrypt(password)
    return cc


def login():
    mp = MasterPassword()
    for i in range(3):
        trust = mp.authenticate()
        if trust:
            return mp.mp_hash
    else:
        Print.fail(">>>  Failed: Too many invalid attempts  <<<")
        sys.exit(1)
