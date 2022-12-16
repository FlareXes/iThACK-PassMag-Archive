from dataclasses import dataclass


@dataclass
class Account:
    acc_id: int
    site: str
    username: str
    url: str


@dataclass
class CipherConfig:
    ciphertext: bytes
    salt: bytes
    tag: bytes
    nonce: bytes
