from Password_Manager.User._db_manager import storePassword, deletePassword, showWebsites, storeEncryptionComponents, getPasswordComponents, updateDatabaseWithNewMasterPassword
from Password_Manager.User._master_encryption import passwordHasher
from Password_Manager._Authenticate import checkTrust
from Password_Manager.User._data_encryption import encryptPassword, decryptPassword
from Password_Manager.Backup.Local_Backup._local_backup import backup_Database_And_Config, deleteLocalBackup, restore
from Password_Manager.Backup.Local_Backup._preference_local_backup import preferredLocalBackup, preferredLocalRestore
from Password_Manager.Backup.Cloud_Backup._cloud_backup import backup_Database_And_Config_On_Cloud, deleteCloudBackup
from Password_Manager.Backup.Cloud_Backup._cloud_cred_manager import cloud_credential_setup
from Password_Manager.Haveibeenpwned._haveibeenpwned import managePwnedPasswords
from Password_Manager.Advance_Features import _csv_password_import, _csv_password_export
from Password_Manager.Essentials.network import checkInternet
from Password_Manager.PasswordGenerator._password_generator import passwordGenerator
from Password_Manager.Essentials.utilities import ask_directory_location, ask_file_location
from prettytable import PrettyTable
from pandas import read_csv
from colorama import Style
from colorama import Fore
import pyperclip
import json
import os

def menu():
    print('''
1.  See password
2.  Add a new password
3.  Delete existing password
4.  View existing details password
5.  Change Master Password
6.  Backup
7.  Export Passwords Into CSV
8.  Import Password From CSV
9.  Dark Web Monitoring
10. Start ClipSite
11. Generate Secure Password
Q.  Exit
''')
    return input(": ")


def backupMenu():
    print('''
    1. Offline Local Backup
    2. Restore Backup
    3. Stop Passwords Backup

    4. Setup Cloud Backup
    5. Cloud Backup (Useful For Sync)
    6. Restore Cloud Backup
    7. Stop Cloud Backup

    8. User Preferrd Backup
    9. Restore Backup From Preferred Location

    10. Setup Both Local And Cloud Backup (Unstable, Under Dev.)
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
    if showWebsites() != 0:
        acc_id = input("\n [*] Please Enter Your Account ID To Delete: ")
        warn = input("\n ⚠  Are you sure you want to delete (y/n): ")

        if warn == "y" or warn == "yes":
            deletePassword(acc_id)
            showWebsites()
        elif warn == "n" or warn == "no":
            print("\n 💯 Safely Canceled")
        else:
            print("\n 👋👋👋👋👋👋👋👋👋 Invalid Input!! Get Out 👉 👋👋👋👋👋👋👋👋👋")
    else:
        print("\nNothing to delete. First feed me some info 🤳😃😜")


def showPassword():
    masterPassword = checkTrust()

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
    try:
        connCheck = checkInternet()
        if connCheck ==True:
            backup_Database_And_Config_On_Cloud()
            with open("Password_Manager/config.json", "r+") as config_file:
                isAutoBackupAllowed = json.load(config_file)
                isAutoBackupAllowed['Automatic Cloud Backup'] = True
                config_file.seek(0)
                json.dump(isAutoBackupAllowed, config_file)
                config_file.truncate()

                print("\n👌 All Passwords Have Been Backed Up On Cloud 📌")
                print("\n👌 From Next Time All Passwords Automaticly Will Be Backed Up On Cloud 📌")
        else:
            print("\n❌❌❌ Internet Connection Required ❌❌❌")

    except Exception as e:
        print(e)
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Unable To Backup On Cloud ❌❌❌")


def cloudSetup():
    if os.path.exists("Password_Manager\Config\cloud_cred.json"):
            warn_choose = input("\nWARNING... WARNING... WARNING... Overwrite Existence Credential Files (y/n): ")
            if warn_choose == "y" or warn_choose == "yes":
                cloud_credential_setup()
            else:
                print("❌ Process Canceled ❌")
    else:
        cloud_credential_setup()



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
    try:
        connCheck = checkInternet()
        if connCheck == True:
            print("\n [*] By proceeding feather YOU WILL LOST ALL YOUR CLOUD BACKUP")
            warn = input("\n ⚠  Are you sure you want to delete (y/n): ")

            if warn == "y" or warn == "yes":
                deleteCloudBackup()
            elif warn == "n" or warn == "no":
                print("\n 💯 Safely Canceled")
            else:
                print("\n 👋👋👋👋👋👋👋👋👋 Invalid Input!! Get Out 👉 👋👋👋👋👋👋👋👋👋")
        else:
            print("\n❌❌❌ Internet Connection Required ❌❌❌")

    except Exception as e:
        print("\n❌❌❌ ErRoR OcCuRrEd 👉 Can't Stop And Delete Cloud Backup ❌❌❌")

def restoreLocalBackup():
    restore()
    print("\n🤞 Successfully Restored To The Previous Stage 🐬")


def changeMasterPassword():
    try:
        oldMasterPassword = checkTrust()
        newMasterPassword = input("\n[+] New Enter Master Password: ")
        conf_new_master_password = input("\n[+] Confirm New Password: ")

        if conf_new_master_password == newMasterPassword:
            updateDatabaseWithNewMasterPassword(oldMasterPassword, newMasterPassword)
            passwordHasher(newMasterPassword)
            if os.path.exists("config.json"):
                with open("config.json", "r") as config_file:
                    isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
                if isAutoBackupAllowed == True:
                    backup()
            print("\nPassword Has Changed Successfully ✔ 🤞")
        else:
            print("\n[-] Process Unsuccessful. Password Didn't Matched")

    except Exception as e:
        print("\n❌❌❌ [-] Process Unsuccessful. Unable To Change Master Password ❌❌❌")


def checkPwnedPasswords():
    try:
        connCheck = checkInternet()
        if connCheck == True:
            result = managePwnedPasswords()
            if result != None: print(result)
        else:
            print("\n❌❌❌ Internet Connection Required ❌❌❌")
    except Exception as e:
        print("\n❌❌❌ [-] Process Unsuccessful. Unable To Check Pwned Passwords ❌❌❌")


def exportEntriesCsv():
    export_location = ask_directory_location()
    print(f"\n[+] Export Location: {export_location}/iThACK-PassMag-export.csv")
    _csv_password_export.export_tocsv(export_location)
    print("\nSuccessfully🤞 Exported All Passwords Into export.csv")


def importCsv():
    filelocation = ask_file_location()
    if filelocation.endswith(".csv"):
        csv = read_csv(filelocation)
        csv.fillna("", inplace=True)
        _csv_password_import.storeCsv(csv)
        print("\n✌✌✌ Passwords Imported Successfully ✌✌✌")
    else:
        print("\n🤔 File Must Be CSV!! Get Out 👉 👋👋👋👋👋👋👋👋👋\n")


def userPreferredBackup():
    preferredLocalBackup()

    print("\n    🤞 Successfully Stored To Preferred Location 🐬")
    print("\n    ⚠ ⚠ ⚠  Please Take Care Of Backup Files That Colud Potentially Leak Your Credentials ⚠ ⚠ ⚠")


def userPreferredRestore():
    preferredLocalRestore()
    print("\n    🤞 Passwords Restored Successfully 🐬")


def startClipSite():
    os.system("start python clipPassMag.py")


def generatePassword():
    print("\n🎯 Minimum Password Length Must Be 👉 8")
    try:
        passLen = int(str(input("\nPassword Length 👉 ")))
        if passLen >= 8:
            password = passwordGenerator(passLen)
            pyperclip.copy(password)
            print("\n🤞 Password is copied to clipboard 😀😀 👇")
            print(f"\n👍 Your {passLen} digit password: ", password)
        else:
            password = passwordGenerator(8)
            print("\n🤞 Password is copied to clipboard  ✔ ✔ ✔")
            pyperclip.copy(password)
            print("\n👍 Your 8 digit password: ", password)
    except ValueError:
            password = passwordGenerator(8)
            print("\n🤞 Password is copied to clipboard  ✔ ✔ ✔")
            pyperclip.copy(password)
            print("\n👍 Your 8 digit password: ", password)
    except Exception as e:
        print(e)