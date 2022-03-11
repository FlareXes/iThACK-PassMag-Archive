import os
import json
from typing import Dict
from Password_Manager.Backup.Local_Backup import _local_backup
from Password_Manager.Backup.Local_Backup import _preference_local_backup
from Password_Manager.User._user_db import create_database

SALT = "Password_Manager/User/masterlevel/00003.1.SALT.bin"
KEY = "Password_Manager/User/masterlevel/00003.1.KEY.bin"
DATABASE = "Password_Manager/User/leveldb/user.db"
CONFIG = "Password_Manager/Config/config.json"


def available_files() -> Dict[str, bool]:
    files_available = {'salt': False, 'key': False, 'database': False, 'config': False}
    if os.path.exists(SALT):
        files_available['salt'] = True
    if os.path.exists(KEY):
        files_available['key'] = True
    if os.path.exists(DATABASE):
        files_available['database'] = True
    if os.path.exists(CONFIG):
        files_available['config'] = True
    return files_available


class checkBackup:
    def isLocalBackupAllowed(self):
        with open("Password_Manager/Config/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
        return isAutoBackupAllowed

    def isCloudBackupAllowed(self):
        with open("Password_Manager/Config/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Cloud Backup']
        return isAutoBackupAllowed

    def isPreferredBackupAllowed(self):
        with open("Password_Manager/Config/config.json", "r") as config_file:
            isPreferredBackupAllowed = json.load(config_file)['User Preferred Local Backup']
        return isPreferredBackupAllowed


def checkConfigurations():
    check = checkBackup()
    files = available_files()

    if not os.path.exists(CONFIG):
        data = {
            'Installation': True,
            'Automatic Backup': False,
            'Automatic Cloud Backup': False,
            'User Preferred Local Backup': False,
        }
        with open(CONFIG, "w") as config_file:
            json.dump(data, config_file)

    # if files['salt'] and files['key'] and files['database'] == False:
    if files['database'] == False and files['key'] and files['salt']:
        create_database()
        print('\nPassword Database Not Found!!! \n'
              'You Have Lost Your All Passwords, So A New Database Has Been Created.\n'
              'Master Password Is Still Same.\n')

    elif not (files['salt'] and files['key'] and files['database']):
        isAutoBackupAllowed = check.isLocalBackupAllowed()
        isPreferredBackupAllowed = check.isPreferredBackupAllowed()

        if isAutoBackupAllowed == True:
            print("\n⚠ Configuration File Not Found ⁉\n")
            askToRestore = input("Restore Backed Up Configuration (y/n): ")

            if askToRestore == "y" or askToRestore == "yes":
                _local_backup.restore()
            elif askToRestore == "n" or askToRestore == "no":
                print("\n 💯 Safely Canceled")
                exit()
            else:
                print("\n❌❌❌ Invalid Input!! ❌❌❌")
                exit()
        elif isPreferredBackupAllowed == True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("EPR Raps\t\tOne More Chance")
            print("\n    User Preference Enabled")
            print("""\nWe have found that you\'ve backup under User Preference Mode. 
            \nSo, you can import that iThACK PassMag Backup Directory.""")
            print("\n[*] Configuration File Not Found\n")

            askToRestore = input("Restore Backup Configurations (y/n): ")
            if askToRestore == "y" or askToRestore == "yes":
                _preference_local_backup.preferredLocalRestore()
            elif askToRestore == "n" or askToRestore == "no":
                print("\n 💯 Safely Canceled")
                exit()
            else:
                print("\n❌❌❌ Invalid Input!! ❌❌❌")
                exit()
        else:
            print('''\nYou Completely Messed Up! With Our Software.
Therefore You Have Lost All Your Passwords Because Their Was Backup Set Up.
You Must Need You Reinstall This Software. Just Run "python _setup.py" Without Quotes.
And Be Aware Next Time, Don't Forget To Backup Your Passwords With iThACK PassMag Functionality.\n
Best Wishes From Whole iThACK PassMag Team. Hmmm...Also Sorry For Inconvenience And Your Lose.\n''')
            exit()