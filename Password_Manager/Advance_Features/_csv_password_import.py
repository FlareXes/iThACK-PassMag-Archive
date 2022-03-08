from turtle import pen
from Password_Manager._Authenticate import checkTrust
from Password_Manager.User._data_encryption import encryptPassword
from Password_Manager.User._db_manager import storePassword, storeEncryptionComponents

def csv_encrypter(cred_csv):
    print("\n[*] Encrypting CSV Passwords")

    master_password = checkTrust()
    passwords = cred_csv['Password']
    passwordsCipher = []
    passwordsComponentes  = []
    
    for password in passwords:
        enc_pass = encryptPassword(str(password), master_password)
        cipher_text = enc_pass['cipher_text']
        salt = enc_pass['salt']
        nonce = enc_pass['nonce']
        tag = enc_pass['tag']

        passwordsCipher.append(cipher_text)
        passwordsComponentes.append(salt + nonce + tag)

    cred_csv.drop(['ID', 'Password'], axis=1, inplace=True)
    cred_csv['Cipher'] = passwordsCipher
    cred_csv['Componentes'] = passwordsComponentes
    return cred_csv


def storeCsv(enc_cred_csv):
    print("\n[*] Loading CSV Into Database")
    encryCSV = csv_encrypter(enc_cred_csv)
    entriesList = encryCSV.values.tolist()
    for entryList in entriesList:
        storedEntryID = storePassword(web_name=entryList[0], url=entryList[1], username=entryList[2], 
                    email=entryList[3], password=entryList[5], description=entryList[4])

        storeEncryptionComponents(entryID=storedEntryID, encryptionComponents=entryList[6])