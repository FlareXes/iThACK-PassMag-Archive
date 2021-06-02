from Password_Manager.Backup.Local_Backup import _local_backup
import json
import os

class checkBackup:
    def isLocalBackupAllowed():
        with open("Password_Manager/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
        return isAutoBackupAllowed

    def isCloudBackupAllowed():
        with open("Password_Manager/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Cloud Backup']
        return isAutoBackupAllowed


def checkConfigurations():
    userSalt = "Password_Manager/User/masterlevel/00003.1.SALT.bin"
    userKey = "Password_Manager/User/masterlevel/00003.1.KEY.bin"
    userDatabase = "Password_Manager/User/leveldb/user.db"
    configFile = "Password_Manager/config.json"

    if not os.path.exists(configFile):
        data = {
        'Automatic Cloud Backup': False,
        'Automatic Backup': False,
        }
        with open("Password_Manager/config.json", "w") as config_file:
            json.dump(data, config_file)


    isAutoBackupAllowed = checkBackup.isLocalBackupAllowed()
    if not os.path.exists(userSalt and userKey and userDatabase):
        if isAutoBackupAllowed == True:
            print("\n⚠ Configuration File Not Found ⁉\n")
            askToRestore = input("Restore Backed Up Configuration (y/n): ")
            
            if askToRestore == "y" or askToRestore == "yes":
                _local_backup.restore("masterpassword")
                _local_backup.restore("passworddatabase")
                print("\n[+] Restore Successful ✔ ✔ ✔")
            elif askToRestore == "n" or askToRestore == "no":
                print("\n 💯 Safely Canceled")
                exit()
            else:
                print("\n❌❌❌ Invalid Input!! ❌❌❌")
                exit()
        else:
            print('''\nYou Completely Messed Up! With Our Software.
Therefore You Have Lost All Your Passwords Because Their Was Backup Set Up.
You Must Need You Reinstall This Software. Just Run "python _install.py" Without Quotes.
And Be Aware Next Don't Forget To Backup Your Passwords With iThACK PassMag Functionality.\n
Best Wishes From Whole iThACK PassMag Team. Hmmm...Also Sorry For In Inconvenience And Your Lose.\n''')
            exit()