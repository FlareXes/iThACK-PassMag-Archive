from Password_Manager.User._db_manager import storePassword, deletePassword, showWebsites, storeEncryptionComponents, getPasswordComponents, updateDatabaseWithNewMasterPassword, exportPasswords
from Password_Manager.User._master_encryption import passwordHasher
from Password_Manager._Authenticate import checkTrust, verifyMasterPassword
from Password_Manager.User._data_encryption import encryptPassword, decryptPassword
from Password_Manager.Backup.Local_Backup._local_backup import backup_Database_And_Config, deleteLocalBackup, restore
from Password_Manager.Backup.Cloud_Backup._cloud_backup import backup_Database_And_Config_On_Cloud, deleteCloudBackup
from Password_Manager.Haveibeenpwned._haveibeenpwned import managePwnedPasswords
from Password_Manager.Importpassword import _csv_password_importer
from prettytable import PrettyTable
from pandas import read_csv
from colorama import Style
from colorama import Fore
import pyperclip
import colorama
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
8. Dark Web Monitoring
9. Import Password From CSV
Q. Exit
''')
    return input(": ")


def backupMenu():
    print('''
    1. Offline Local Backup
    2. Restore Backup
    3. Stop Passwords Backup

    4. Cloud Backup (Useful For Sync)
    5. Restore Cloud Backup
    6. Stop Cloud Backup
    7. Setup Both Local And Cloud Backup
    Q. Go Back
    ''')
    return input("    : ")


def addEntry():
    masterPassword = checkTrust()

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

    if showWebsites() != 0:
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
    else:
        print("\nNothing to see. First feed me some info 🤳😃😜")


def showEntries():
    showWebsites()


def backup():
    backup_Database_And_Config()
    with open("Password_Manager/config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Backup'] = True
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()

        print("\n👌 All Passwords Have Been Backed Up On Local System 📌")
        print("\n👌 From Next Time All Passwords Automatically Will Be Backed Up 📌")


def cloudBackup():
    backup_Database_And_Config_On_Cloud()
    with open("Password_Manager/config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Cloud Backup'] = True
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()

        print("\n👌 All Passwords Have Been Backed Up On Cloud 📌")
        print("\n👌 From Next Time All Passwords Automaticly Will Be Backed Up 📌")


def stopLocalBackup():
    print("\n [*] By proceeding feather YOU WILL LOST ALL YOUR BACKED UP PASSWORDS")
    warn = input("\n ⚠  Are you sure you want to delete (y/n): ")

    if warn == "y" or warn == "yes":
        deleteLocalBackup()
    elif warn == "n" or warn == "no":
        print("\n 💯 Safely Canceled")
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 Invalid Input!! Get Out 👉 👋👋👋👋👋👋👋👋👋")


def stopCloudBackup():
    print("\n [*] By proceeding feather YOU WILL LOST ALL YOUR CLOUD BACKUP")
    warn = input("\n ⚠  Are you sure you want to delete (y/n): ")

    if warn == "y" or warn == "yes":
        deleteCloudBackup()
    elif warn == "n" or warn == "no":
        print("\n 💯 Safely Canceled")
    else:
        print("\n 👋👋👋👋👋👋👋👋👋 Invalid Input!! Get Out 👉 👋👋👋👋👋👋👋👋👋")


def restoreLocalBackup():
    restore()
    print("\n🤞 Successfully Restored To The Previous Stage 🐬")


def changeMasterPassword():
    print("\nCurrent Password (Verify Yourself) 📌\n")
    oldMasterPassword = checkTrust()
    newMasterPassword = input("\n[+] New Enter Master Password: ")
    updateDatabaseWithNewMasterPassword(oldMasterPassword, newMasterPassword)
    passwordHasher(newMasterPassword)
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
        if isAutoBackupAllowed == True:
            backup()
    print("\nPassword Has Changed Successfully ✔ 🤞")


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


def checkPwnedPasswords():
    test = managePwnedPasswords()
    print(test)


def importCsv():
    # connection = connect_database()
    # myCursor = connection.cursor()

    csv = read_csv('export.csv')
    cpCSV = csv.copy()
    cpCSV.fillna("", inplace=True)
    del(csv)

    _csv_password_importer.storeCsv(cpCSV)
    print("\n✌✌✌ Passwords Importred Successfully ✌✌✌")