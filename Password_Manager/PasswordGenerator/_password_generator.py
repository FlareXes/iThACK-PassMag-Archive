from random import shuffle
import string
import secrets

def passwordConfiguration(length: int) -> int:
    eacher = int(length/4)
    return eacher

def passwordGenerator(length: int) -> str:
    eacher = passwordConfiguration(length)
    possibleLowerCase = string.ascii_lowercase
    possibleUpperCase = string.ascii_uppercase
    possiblePunctuations = string.punctuation
    possibleDigits = string.digits

    salt = list(''.join(secrets.choice(possibleLowerCase) for i in range(eacher)) + ''.join(secrets.choice(possibleUpperCase) for i in range(eacher)) + ''.join(secrets.choice(possibleDigits) for i in range(eacher)) + ''.join(secrets.choice(possiblePunctuations) for i in range((length - eacher*3))))
    shuffle(salt)
    return ''.join(salt)


# TODO: Don't Use Similar Char
