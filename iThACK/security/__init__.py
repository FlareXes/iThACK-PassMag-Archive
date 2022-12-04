from iThACK.security.AES import AES256


def getpass(mp_hash):
    password = input("Password: ")
    aes = AES256(mp_hash)
    cc = aes.encrypt(password)
    return cc
