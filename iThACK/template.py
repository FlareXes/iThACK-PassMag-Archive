class Account:
    def __init__(self, acc_id: int, site: str, username: str, url: str):
        self.acc_id = acc_id
        self.site = site
        self.username = username
        self.url = url


class CipherConfig:
    def __init__(self, ciphertext: bytes, salt: bytes, tag: bytes, nonce: bytes):
        self.ciphertext = ciphertext
        self.salt = salt
        self.tag = tag
        self.nonce = nonce
