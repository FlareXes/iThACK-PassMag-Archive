from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes


def salt(length: int) -> bytes:
    return get_random_bytes(length)


def kdf_scrypt(key: bytes, _salt: bytes):
    cost_factor = 2 ** 14
    rounds = 8
    parallel_factor = 1
    key_length = 32  # bytes
    return scrypt(password=str(key), salt=str(_salt), key_len=key_length, N=cost_factor, r=rounds, p=parallel_factor)
