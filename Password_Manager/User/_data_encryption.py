from Cryptodome.Cipher import AES
from Password_Manager.User._master_encryption import saltGenrator
import hashlib
from base64 import b64encode, b64decode

def encryptPassword(password, masterpassword):
    try:
        salt = saltGenrator()

        PrivateKey = hashlib.scrypt(masterpassword.encode('utf-8'), salt=salt, n=2**14,  r=8, p=1, dklen=32)

        # cipher config
        cipher_config = AES.new(PrivateKey, AES.MODE_GCM)

        # return dictonary with the encrypted text
        cipher_text, tag = cipher_config.encrypt_and_digest(bytes(password, 'utf-8'))

        encryptionComponents = {
            'cipher_text': b64encode(cipher_text).decode('utf-8'),
            'salt': b64encode(salt).decode('utf-8'),
            'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
            'tag': b64encode(tag).decode('utf-8'),
        }

        return encryptionComponents
    except Exception as e:
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Can't Encrypt Data  ❌❌❌")



def decryptPassword(cipher_text, salt, nonce, tag, password):
    try:
        salt = b64decode(salt)
        cipher_text = b64decode(cipher_text)
        nonce = b64decode(nonce)
        tag = b64decode(tag)

        private_key = hashlib.scrypt(password.encode('utf-8'),salt=salt, n=2**14, p=1, r=8, dklen=32)

        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        decrypted = cipher.decrypt_and_verify(cipher_text, tag)

        return decrypted
    except Exception as e:
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Can't Decrypt Data ❌❌❌")
