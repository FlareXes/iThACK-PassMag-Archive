import os.path
from typing import Tuple

from iThACK import LEVELDB_DIR
from iThACK.security.utils import salt, kdf_scrypt

from getpass import getpass
from secrets import compare_digest


class MasterPassword:
    def __init__(self):
        salt_file = "SALT.0.1V.bin"
        key_file = "KEY.0.1V.bin"

        self.salt_loc = os.path.join(LEVELDB_DIR, salt_file)
        self.key_loc = os.path.join(LEVELDB_DIR, key_file)

    def _save(self, key: bytes, _salt: bytes) -> None:
        with open(self.key_loc, "wb") as f:
            f.write(key)

        with open(self.salt_loc, "wb") as f:
            f.write(_salt)

    def get(self) -> Tuple:
        with open(self.key_loc, "rb") as f:
            key = f.read()

        with open(self.salt_loc, "rb") as f:
            _salt = f.read()

        return key, _salt

    def generate_new(self):
        _salt = salt(32)
        key = kdf_scrypt(getpass("Master Key: "), _salt)
        self._save(key, _salt)

    def authenticate(self):
        key, _salt = self.get()
        new_key = kdf_scrypt(getpass("Master Key: "), _salt)

        validity = compare_digest(key, new_key)
        return validity
