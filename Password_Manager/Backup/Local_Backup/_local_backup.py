import shutil
from pathlib import Path
import glob
import os
import json

def backup_Database_And_Config():
    # create path, if it doesn't exist'
    location = Path("C:\\ProgramData\\iThACK PassMag")
    location.mkdir(parents=True, exist_ok=True)
    
    # copy database from leveldb
    shutil.copy("Password_Manager/User/leveldb/user.db", location)
    
    # copy all file from masterlevel
    files_to_backup = glob.glob("Password_Manager/User/masterlevel/*.bin")
    for filename in files_to_backup:
        shutil.copy(filename, location)


def restore(whatToBackup):
    '''
    This function will restore previously backed up master password files and password database.
    '''
    if whatToBackup == "masterpassword":
        backedUp_key = "C:\\ProgramData\\iThACK Passmag\\00003.1.KEY.bin"
        backedUp_salt = "C:\\ProgramData\\iThACK Passmag\\00003.1.SALT.bin"

        restoreFileLocation = Path("Password_Manager/User/masterlevel")
        restoreFileLocation.mkdir(parents=True, exist_ok=True)

        if os.path.exists(backedUp_key and backedUp_salt):
            shutil.copy(backedUp_key,restoreFileLocation)
            shutil.copy(backedUp_salt,restoreFileLocation)
        else:
            print("\n❌ Backup Configuration Not Found 📌\n")
            exit()

    if whatToBackup == "passworddatabase":
        backedUp_database = "C:\\ProgramData\\iThACK Passmag\\user.db"

        restoreFileLocation = Path("Password_Manager/User/leveldb")
        restoreFileLocation.mkdir(parents=True, exist_ok=True)

        if os.path.exists(backedUp_database):
            shutil.copy(backedUp_database,restoreFileLocation)
        else:
            print("\n❌ Backup Configuration Not Found 📌\n")
            exit()

def deleteLocalBackup():
    print('\n❌✌❌ deleting backup ❌✌❌')

    backedUp_config = "C:\\ProgramData\\iThACK Passmag"
    if os.path.exists(backedUp_config):
        shutil.rmtree(backedUp_config)

    with open("Password_Manager/config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Backup'] = False
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()
    print("\n[-] records deleted")