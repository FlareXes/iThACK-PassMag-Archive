import User._local_backup
import json
import os

def checkConfigurations():
    userSalt = "User/masterlevel/00003.1.SALT.bin"
    userKey = "User/masterlevel/00003.1.KEY.bin"
    userDatabase = "User/leveldb/user.db"
    configFile = "config.json"

    if not os.path.exists(configFile):
        data = {
        'Automatic Cloud Backup': False,
        'Automatic Backup': False,
        }
        with open("config.json", "w") as config_file:
            json.dump(data, config_file)


    with open("config.json", "r") as config_file:
        isAutoBackupAllowed = json.load(config_file)['Automatic Backup']

    if isAutoBackupAllowed == True:
        if not os.path.exists(userSalt and userKey and userDatabase):
            print("\n⚠ Configuration File Not Found ⁉\n")
            askToRestore = input("Restore Backed Up Configuration (y/n): ")
            
            if askToRestore == "y" or askToRestore == "yes":
                User._local_backup.restore("masterpassword")
                User._local_backup.restore("passworddatabase")
                print("\n[+] Restore Successful ✔ ✔ ✔")
            elif askToRestore == "n" or askToRestore == "no":
                print("\n 💯 Safely Canceled")
                exit()
            else:
                print("\n❌❌❌ Invalid Input!! ❌❌❌")
    else:
        print("\n❌❌❌ Configuration File Not Found ❌❌❌\n")