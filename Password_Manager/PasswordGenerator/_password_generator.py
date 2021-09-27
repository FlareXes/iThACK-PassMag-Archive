from random import shuffle
import string
import secrets

def passwordConfiguration(length: int) -> int:
    eacher = int(length/4)
    possibleLowerCase = string.ascii_lowercase
    possibleUpperCase = string.ascii_uppercase
    possiblePunctuations = string.punctuation
    possibleDigits = string.digits
    
    return eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations

def passwordGenerator_Type_1(length: int) -> str:
    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(length)

    salt = list(''.join(secrets.choice(possibleLowerCase) for i in range(eacher)) + ''.join(secrets.choice(possibleUpperCase) \
        for i in range(eacher)) + ''.join(secrets.choice(possibleDigits) for i in range(eacher)) + \
            ''.join(secrets.choice(possiblePunctuations) for i in range((length - eacher*3))))
    shuffle(salt)
    return ''.join(salt)


def passwordGenerator_Type_2(length: int) -> str:
    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(length)

    lower = set()
    upper = set()
    punct = set()
    digit = set()
    while len(lower) != eacher:
        lower.add(secrets.choice(possibleLowerCase))


    while len(upper) != eacher:
        upper.add(secrets.choice(possibleUpperCase))


    while len(punct) != eacher:
        punct.add(secrets.choice(possibleDigits))


    while len(digit) != eacher:
        digit.add(secrets.choice(possiblePunctuations))


    characterSet = list(lower | upper | digit | punct)                       # or a.union(b)
    shuffle(characterSet)
    return ''.join(characterSet)