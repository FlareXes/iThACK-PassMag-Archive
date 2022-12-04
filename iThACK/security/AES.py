from Cryptodome.Cipher import AES

from iThACK.security.utils import kdf_scrypt, salt
from iThACK.template import CipherConfig
from iThACK.utils import attrs


class AES256:
    def __init__(self, master_password_hash):
        self.mp = master_password_hash

    def encrypt(self, data: str):
        data = data.encode("utf-8")
        _salt = salt(32)

        key = kdf_scrypt(self.mp, _salt)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return CipherConfig(ciphertext, _salt, tag, cipher.nonce)

    def decrypt(self, cc: CipherConfig):
        ciphertext, _salt, tag, nonce = attrs(cc)

        key = kdf_scrypt(self.mp, _salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
        return data
