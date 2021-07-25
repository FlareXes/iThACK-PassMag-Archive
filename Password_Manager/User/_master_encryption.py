import string
import secrets
import hashlib
import json
import os

def storeKeySalt(salt, key):
    if os.path.exists("Password_Manager/User/masterlevel"):
        with open("Password_Manager/User/masterlevel/00003.1.SALT.bin", "wb") as saltfile:
            saltfile.write(salt)
        
        with open("Password_Manager/User/masterlevel/00003.1.KEY.bin", "wb") as saltfile:
            saltfile.write(key)
    else:
        os.mkdir("Password_Manager/User/masterlevel")
        with open("Password_Manager/User/masterlevel/00003.1.SALT.bin", "wb") as saltfile:
            saltfile.write(salt)
        
        with open("Password_Manager/User/masterlevel/00003.1.KEY.bin", "wb") as saltfile:
            saltfile.write(key)


def saltGenrator():
    try:
        alphabet = string.ascii_letters + string.digits  + string.punctuation
        while True:
            salt = ''.join(secrets.choice(alphabet) for i in range(89))
            if (sum(c.islower() for c in salt) >=19) and (sum(c.isupper() for c in salt) >=19) and (sum(c.isdigit() for c in salt)>=10):
                break
        return salt.encode('utf-8')
    except Exception as e:
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Can't Generate Salt ❌❌❌")



def passwordHasher(password):
    try:
        salt = saltGenrator()
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 150000, dklen=128)
        storeKeySalt(salt, key)
    except Exception as e:
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Unable To Hash The Password ❌❌❌")


if __name__ == '__main__':
    print("\n❌❌❌ Don't Mess With Internal Files Otherwise You May Loss Your Data ❌❌❌")
    print("\n❌❌❌ Sorry! You can not run this file directly ❌❌❌\n")
    exit()

# https://docs.python.org/3/library/hashlib.html?highlight=hash
# https://docs.python.org/3/library/secrets.html?highlight=secure%20random
# https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/
# https://docs.python.org/3/library/hmac.html?highlight=hash