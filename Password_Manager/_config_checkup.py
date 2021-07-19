import os
import json
from Password_Manager.Backup.Local_Backup import _local_backup
from Password_Manager.Backup.Local_Backup import _preference_local_backup

class checkBackup:
    def isLocalBackupAllowed(self):
        # with open(self.configFile, "r") as config_file:
        with open("Password_Manager/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Backup']
        return isAutoBackupAllowed

    def isCloudBackupAllowed(self):
        with open("Password_Manager/config.json", "r") as config_file:
            isAutoBackupAllowed = json.load(config_file)['Automatic Cloud Backup']
        return isAutoBackupAllowed
    
    def isPreferredBackupAllowed(self):
        with open("Password_Manager/config.json", "r") as config_file:
            isPreferredBackupAllowed = json.load(config_file)['User Preferred Local Backup']
        return isPreferredBackupAllowed


def checkConfigurations():
    userSalt = "Password_Manager/User/masterlevel/00003.1.SALT.bin"
    userKey = "Password_Manager/User/masterlevel/00003.1.KEY.bin"
    userDatabase = "Password_Manager/User/leveldb/user.db"
    configFile = "Password_Manager/config.json"

    if not os.path.exists(configFile):
        data = {
        'Installation': True,
        'Automatic Backup': False,
        'Automatic Cloud Backup': False,
        'User Preferred Local Backup': False,
        }
        with open("Password_Manager/config.json", "w") as config_file:
            json.dump(data, config_file)

    check = checkBackup()
    if not (os.path.exists(userSalt) and os.path.exists(userDatabase) and os.path.exists(userKey)):
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

        if isPreferredBackupAllowed == True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print('\t\tOne More Chance 🎏🎏🎏')
            
            print('\n✌ ✌ ✌ User Preference Enabled ✌ ✌ ✌')
            
            print('''\nWe found that you\'ve backed up for file under User Preference Mode. 
            \nSo, you can import that iThACK PassMag Backup Directory.''')
            
            print("\n⚠ Configuration File Not Found ⁉\n")
            askToRestore = input("Restore Backed Up Configuration (y/n): ")
            
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
You Must Need You Reinstall This Software. Just Run "python _install.py" Without Quotes.
And Be Aware Next Time, Don't Forget To Backup Your Passwords With iThACK PassMag Functionality.\n
Best Wishes From Whole iThACK PassMag Team. Hmmm...Also Sorry For Inconvenience And Your Lose.\n''')
            exit()