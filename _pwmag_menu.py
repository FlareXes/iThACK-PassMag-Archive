from _db_manager import storePassword, deletePassword, showWebsites, storeEncryptionComponents, getPasswordComponents, updateDatabaseWithNewMasterPassword, exportPasswords
from User._master_encryption import passwordHasher
from _Authenticate import checkTrust, verifyMasterPassword
from User._data_encryption import encryptPassword, decryptPassword
from User._local_backup import backup_Database_And_Config
from Cloud_User._cloud_backup import backup_Database_And_Config_On_Cloud
from prettytable import PrettyTable
import pyperclip
import json
import os

def menu():
    print('''
        1. See password
        2. Add a new password
        3. Delete existing password
        4. View existing details password
        5. Change Master Password
        6. Backup
        7. Export Passwords Into CSV
        Q. Exit
        ''')
    return input("    : ")


def backupMenu():
    print('''
    1. Offline Local Backup
    2. Cloud Backup (Useful For Sync)
    3. Setup Both Local And Cloud Backup
    4. Restore Backup
    5. Stop Passwords Backup
    Q. Go Back
    ''')
    return input("    : ")


def addEntry():
    masterPasswordAttempt = 0
    while masterPasswordAttempt <= 2:
        masterPassword = input("\nVerify Yourself To Continue (Master Password)📌 : ")
        if verifyMasterPassword(masterPassword) == True:
            break
        else:
            print("\n❌ Nope, Try Again ❌")
            masterPasswordAttempt += 1
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 To Many Invalid Attempts!! Get Out 👉 👋👋👋👋👋👋👋👋👋\n")
        quit()

    website = input("\nWebsite/App Name\n: ")

    print("\nWebsite/App: "+ website + "  ➖  Password: " + '' + "  ➖  Username: " + '' + "  ➖  Email: " + '' + "  ➖  URL: " + '')

    PasswordEncryptionComponents = encryptPassword(input("\nPassword\n: "), masterPassword)
    salt = PasswordEncryptionComponents['salt']
    nonce = PasswordEncryptionComponents['nonce']
    tag = PasswordEncryptionComponents['tag']
    password = PasswordEncryptionComponents['cipher_text']

    print("\nWebsite/App: "+ website + "  ➖  Password: " + password + "  ➖  Username: " + '' + "  ➖  Email: " + '' + "  ➖  URL: " + '')

    username = input("\nUsername\n: ")

    print("\nWebsite/App: "+ website + "  ➖  Password: " + password + "  ➖  Username: " + username + "  ➖  Email: " + '' + "  ➖  URL: " + '')

    email = input("\nE-Mail\n: ")

    print("\nWebsite/App: "+ website + "  ➖  Password: " + password + "  ➖  Username: " + username + "  ➖  Email: " + email + "  ➖  URL: " + '')

    url = input("\nURL\n: ")

    print("\nWebsite/App: "+ website + "  ➖  Password: " + password + "  ➖  Username: " + username + "  ➖  Email: " + email + "  ➖  URL: " + url + "    ✔")

    description = input("\nDescription\n: ")

    storedEntryID = storePassword(website, url, username, email, password, description)   # Pattern Should Be This websiteName, websiteURL, username, email, password, description

    storeEncryptionComponents(storedEntryID, salt+nonce+tag)
    showWebsites()

    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
        if isAutoBackupAllowed == True:
            backup()


def deleteEntry():
    checkTrust()
    showWebsites()
    acc_id = input("\n [*] Please Enter Your Account ID To Delete: ")
    warn = input("\n ⚠  Are you sure you want to delete (y/n): ")

    if warn == "y" or warn == "yes":
        deletePassword(acc_id)
        showWebsites()
    elif warn == "n" or warn == "no":
        print("\n 💯 Safely Canceled")
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 Invalid Input!! Get Out 👉 👋👋👋👋👋👋👋👋👋")


def showPassword():
    masterPasswordAttempt = 0
    while masterPasswordAttempt <= 2:
        masterPassword = input("\nVerify Yourself To Continue (Master Password)📌 : ")
        if verifyMasterPassword(masterPassword) == True:
            break
        else:
            print("\n❌ Nope, Try Again ❌")
            masterPasswordAttempt += 1
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 To Many Invalid Attempts!! Get Out 👉 👋👋👋👋👋👋👋👋👋\n")
        quit()

    showWebsites()

    acc_id = input("\n [+] Please Enter Your Account ID To See Password: ")
    encryptionComponents = getPasswordComponents(acc_id)
    cipher_text = encryptionComponents[:-168]
    salt = encryptionComponents[-168:-48]
    nonce = encryptionComponents[-48:-24]
    tag = encryptionComponents[-24:]

    decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, masterPassword).decode('utf-8')   # Pattern should be (cipher_text, salt, nonce, tag, password)
    # Adding decryptedPassword To Column
    myTable = PrettyTable()
    myTable.add_column("Password", [decryptedPassword * 4])
    print(myTable)

    print("\n🤞 Password is copied to clipboard  ✔ ✔ ✔")
    pyperclip.copy(decryptedPassword)


def changeMasterPassword():
    print("\nCurrent Password (Verify Yourself) 📌\n")
    oldMasterPassword = checkTrust()
    newMasterPassword = input("\n[+] New Enter Master Password: ")
    updateDatabaseWithNewMasterPassword(oldMasterPassword, newMasterPassword)
    passwordHasher(newMasterPassword)
    print("\nPassword Has Changed Successfully ✔🤞")


def backup():
    backup_Database_And_Config()
    with open("config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Backup'] = True
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()


def cloudBackup():
    backup_Database_And_Config_On_Cloud()
    with open("config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Cloud Backup'] = True
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()


def exportEntriesCsv():
    masterPasswordAttempt = 0
    while masterPasswordAttempt <= 2:
        masterPassword = input("\nVerify Yourself To Continue (Master Password)📌 : ")
        if verifyMasterPassword(masterPassword) == True:
            break
        else:
            print("\n❌ Nope, Try Again ❌")
            masterPasswordAttempt += 1
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 To Many Invalid Attempts!! Get Out 👉 👋👋👋👋👋👋👋👋👋\n")
        quit()

    exportPasswords()
    print("\nSuccessfully🤞 Exported Into export.csv ✔ ✔ ✔")