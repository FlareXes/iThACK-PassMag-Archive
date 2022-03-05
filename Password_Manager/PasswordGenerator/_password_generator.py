from random import shuffle, choice
import string
import secrets
from typing import Optional, Dict, Tuple


def passwordConfiguration(length: int) -> Tuple[int, str, str, str, str]:
    eacher = int(length / 4)
    possibleLowerCase = string.ascii_lowercase
    possibleUpperCase = string.ascii_uppercase
    possiblePunctuations = string.punctuation
    possibleDigits = string.digits
    return eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations


def getType(chr):
    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(0)
    if chr in possibleLowerCase:
        return 'lowercase'
    elif chr in possibleUpperCase:
        return 'uppercase'
    elif chr in possibleDigits:
        return 'digit'
    elif chr in possiblePunctuations:
        return 'punctuation'


def passwordGenerator_Type_1(length: int) -> str:
    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(length)
    salt = list(
        ''.join(secrets.choice(possibleLowerCase) for i in range(eacher))
        + ''.join(secrets.choice(possibleUpperCase) for i in range(eacher))
        + ''.join(secrets.choice(possibleDigits) for i in range(eacher))
        + ''.join(secrets.choice(possiblePunctuations) for i in range((length - eacher * 3))))
    shuffle(salt)
    return ''.join(salt)


def passwordGenerator_Type_2(length: int) -> str:
    """
    max_length -> 43
    """
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

    while len(digit) != (length - eacher * 3):
        digit.add(secrets.choice(possiblePunctuations))

    characterSet = list(lower | upper | digit | punct)  # or a.union(b)
    shuffle(characterSet)
    return ''.join(characterSet)


def passwordGenerator_Type_3(length: int) -> str:
    """
    max_length -> 43
    """
    password = list(passwordGenerator_Type_2(length))
    temp = []
    for i in range(length):
        try:
            if getType(password[i]) == getType(password[i + 1]):
                temp.append(password[i])
                password.remove(password[i])
        except:
            pass

    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(0)
    for i in range(len(temp)):
        lastEntryType = getType(password[-1])
        if lastEntryType != 'lowercase':
            password.append(secrets.choice(possibleLowerCase))

        elif lastEntryType != 'uppercase':
            password.append(secrets.choice(possibleUpperCase))

        elif lastEntryType != 'digit':
            password.append(secrets.choice(possibleDigits))

        elif lastEntryType != 'punctuation':
            password.append(secrets.choice(possiblePunctuations))
    return ''.join(password)


def passwordGenerator_Type_4(length: int) -> str:
    """
    max_length -> 60
    """
    eacher, possibleLowerCase, possibleUpperCase, possibleDigits, possiblePunctuations = passwordConfiguration(length)
    possibleCharecters = possibleLowerCase + possibleUpperCase + possibleDigits + possiblePunctuations
    possibleCharecterSet = list()

    for i in range(len(possibleCharecters)):
        secChar = secrets.choice(possibleCharecters)
        possibleCharecterSet.append(secChar)
        possibleCharecters = possibleCharecters.replace(secChar, '')

    password = []
    for i in range(len(possibleCharecterSet)):
        try:
            if getType(possibleCharecterSet[i]) != getType(possibleCharecterSet[i + 1]):
                password.append(possibleCharecterSet[i])
        except:
            break

    return ''.join(password)[:length]


def passwordGenerator_Type_5(length: int, allowed_types: Optional[Dict[str, bool]] = None) -> str:
    if allowed_types is None:
        allowed_types = {'lowercase': True, 'uppercase': True, 'digit': True, 'punctuation': True}
    possible_characters = passwordConfiguration(length)
    user_preferred_characters_list = []
    counter = 1
    for key, value in allowed_types.items():
        if value:
            user_preferred_characters_list.append(possible_characters[counter])
        counter += 1
    user_preferred_characters = ''.join(user_preferred_characters_list)
    try:
        password = ''.join(secrets.choice(user_preferred_characters) for i in range(length))
    except IndexError:
        return ''
    return password


def passwordGenerator(length: int, allowed_types: Optional[Dict[str, bool]] = None) -> str:
    # try:
    #     if all(allowed_types.values()):
    if length <= 43:
        return choice(
            [passwordGenerator_Type_1(length), passwordGenerator_Type_2(length), passwordGenerator_Type_3(length),
             passwordGenerator_Type_4(length)])
    elif length <= 60:
        return choice([passwordGenerator_Type_1(length), passwordGenerator_Type_4(length)])
    else:
        return passwordGenerator_Type_1(length)
    #     else:
    #         passwordGenerator_Type_5(length, allowed_types)
    # except:
    #     pass

# print(passwordGenerator_Type_5(20, allowed_types = {'lowercase': False, 'uppercase': False, 'digit': True, 'punctuation': True}))
# print(passwordGenerator_Type_5(14, allowed_types = {'lowercase': False, 'uppercase': False, 'digit': False, 'punctuation': False}))
# print(passwordGenerator(16))