import secrets
import string


def charset(bounds: str) -> str:
    chars = ""
    if 'l' in bounds: chars += string.ascii_letters
    if 'd' in bounds: chars += string.digits
    if 'p' in bounds: chars += string.punctuation

    return chars


def random_password(length: int = 16, bounds: str = "ldp") -> str:
    char_set = charset(bounds)
    tmp = True

    while True:
        password = "".join(secrets.choice(char_set) for i in range(length))
        if "l" in bounds:
            tmp = tmp and any(c.isalpha() for c in password)

        if "d" in bounds:
            tmp = tmp and any(c.isdigit() for c in password)

        if "p" in bounds:
            tmp = tmp and any(c in string.punctuation for c in password)

        if tmp:
            break

    return password


if __name__ == "__main__":
    a = random_password(length=32, bounds="ld")
    print(a)
