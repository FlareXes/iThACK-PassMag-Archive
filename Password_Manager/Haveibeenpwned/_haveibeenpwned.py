from hashlib import sha1
import requests
from Password_Manager.User._user_db import connect_database
from Password_Manager.User._data_encryption import decryptPassword
from Password_Manager._Authenticate import checkTrust
import colorama
from colorama import Fore
from colorama import Style
from prettytable import PrettyTable

def getPasswords():
    masterPassword = checkTrust()

    connection = connect_database()
    mycursor = connection.cursor()
    sqlQuery_1 = "SELECT ID, Website, Username, Password FROM UserDataBase"
    mycursor.execute(sqlQuery_1)
    rows_1 = mycursor.fetchall()
    sqlQuery_2 = "SELECT Encryption FROM UserDataBase_Encryption"
    mycursor.execute(sqlQuery_2)
    rows_2 = mycursor.fetchall()

    ExportEntries = []

    for i in range(0, len(rows_1)):
        encryptionComponents = rows_1[i][3]+str(rows_2[i][0])
        cipher_text = encryptionComponents[:-168]
        salt = encryptionComponents[-168:-48]
        nonce = encryptionComponents[-48:-24]
        tag = encryptionComponents[-24:]
        decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, masterPassword).decode('utf-8')
        ExportEntries.append((rows_1[i][0], rows_1[i][1], rows_1[i][2], decryptedPassword))
    
    return ExportEntries


def haveibeenpwned():
    ExportEntries = getPasswords()
    print("\n[+] Please Wait It May Take Time ⌛⏳")
    results = []

    if len(ExportEntries) != 0:
        for entry in ExportEntries:
            password = entry[3]
            hash_5 = (sha1(password.encode('utf-8')).hexdigest()).upper()
            response = requests.get(f'https://api.pwnedpasswords.com/range/{hash_5[0:5]}', headers={'Add-Padding':'true'})
            result = (response.text).find(hash_5[5:])
            if result != -1:
                results.append(entry[0:3])
        return results
    else:
        print("\nYou don't have any password to check. First feed me some info 🤳😃😜")
        return results


def managePwnedPasswords():
    colorama.init()
    pwnedPasswords = haveibeenpwned()

    if len(pwnedPasswords) != 0:
        print(Fore.RED + f'''\nYour below password has appeared in a data breach 
    and should never be used again. Change it.\n''' + Style.RESET_ALL)
        myTable = PrettyTable(["ID", "Website", "Username"])
        for row in pwnedPasswords:
            row = list(row)
            myTable.add_row(row)
        
        return Fore.GREEN + str(myTable) + Style.RESET_ALL