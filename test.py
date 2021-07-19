from pandas import read_csv
from Password_Manager.User._user_db import connect_database
from Password_Manager.User._data_encryption import encryptPassword
from Password_Manager.User._db_manager import storePassword, storeEncryptionComponents


def csv_encrypter(cpCSV):
    print("[*] Encrypting CSV Passwords")
    passwordsCipher = []
    passwordsComponentes  = []
    passwords = cpCSV['Password']

    for password in passwords:
        encPass = encryptPassword(str(password), "plz")
        cipher_text = encPass['cipher_text']
        salt = encPass['salt']
        nonce = encPass['nonce']
        tag = encPass['tag']

        passwordsCipher.append(cipher_text)
        passwordsComponentes.append(salt + nonce + tag)

    cpCSV.drop(['ID', 'Password'], axis=1, inplace=True)
    cpCSV['Cipher'] = passwordsCipher
    cpCSV['Componentes'] = passwordsComponentes
    
    return encryCSV


def storeCsv():
    print("[*] Loading CSV Into Database")
    encryCSV = csv_encrypter()
    entriesList = encryCSV.values.tolist()

    for entryList in entriesList:
        storedEntryID = storePassword(web_name = entryList[0], url = entryList[1], username = entryList[2], 
                    email = entryList[3], password = entryList[5], description=entryList[4])

        storeEncryptionComponents(entryID=storedEntryID, encryptionComponents=entryList[6])


def importCsv():
    connection = connect_database()
    myCursor = connection.cursor()

    csv = read_csv('export.csv')
    cpCSV = csv.copy()
    cpCSV.fillna("", inplace=True)