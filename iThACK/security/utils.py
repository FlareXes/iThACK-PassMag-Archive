from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes


def salt(length: int) -> bytes:
    return get_random_bytes(length)


def kdf_scrypt(key, random_bytes):
    cost_factor = 2 ** 14
    rounds = 8
    parallel_factor = 1
    key_length = 32  # bytes
    return scrypt(password=key, salt=random_bytes, key_len=key_length, N=cost_factor, r=rounds, p=parallel_factor)


def generate_master_password() -> bytes:
    return kdf_scrypt(input("Master Key: "), salt(32))


def get_master_password() -> bytes:
    return kdf_scrypt(input("Master Key: "), salt(32))


def get_mp_hash() -> bytes:
    # Simply hashing master password is insecure so, I added some cost factor.
    static_salt = b"\xb5\x14\xdbKV\xa5Q&\xc5\xef\xfa\x87@]\xa6\xcf?\x8dAn\x97a\x11\xa2\xf0\xae\xa4r\xd7\x0b\xeaY"
    return kdf_scrypt(input("Master Key: "), static_salt)
