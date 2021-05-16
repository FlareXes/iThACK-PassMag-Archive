import hashlib
import secrets


def checkTrust():
    while True:
        masterPassword = input("\n[*] Master Password: ")
        trust = verifyMasterPassword(masterPassword)
        if trust == True:
            print("\nWelcome")
            break
        else:
            print("\nInvalid Attempt\n")
    return masterPassword
    

def verifyMasterPassword(masterPassword):
    with open("User/masterlevel/00003.1.SALT.bin", "rb") as saltFile:
        salt = saltFile.read()
    with open("User/masterlevel/00003.1.KEY.bin", "rb") as keyFile:
        key = keyFile.read()

    new_key = hashlib.pbkdf2_hmac('sha256', masterPassword.encode('utf-8'), salt, 150000,
    dklen=128   # Get a 128 byte key
)
    trust = secrets.compare_digest(key, new_key)
    return trust