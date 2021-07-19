from pathlib import Path
import shutil
import glob
import json
import os

defaultBackedUp_key_location = "C:\\ProgramData\\iThACK Passmag\\00003.1.KEY.bin"
defaultBackedUp_salt_location = "C:\\ProgramData\\iThACK Passmag\\00003.1.SALT.bin"
defaultBackedUp_database_location = "C:\\ProgramData\\iThACK Passmag\\user.db"
defaultBackupPath="C:\\ProgramData\\iThACK PassMag"

def backup_Database_And_Config(backupPath=defaultBackupPath):
    # create path, if it doesn't exist'
    location = Path(backupPath)
    location.mkdir(parents=True, exist_ok=True)
    
    # copy database from leveldb
    shutil.copy("Password_Manager/User/leveldb/user.db", location)
    
    # copy all file from masterlevel
    files_to_backup = glob.glob("Password_Manager/User/masterlevel/*.bin")
    for filename in files_to_backup:
        shutil.copy(filename, location)


def restore(backedUp_key=defaultBackedUp_key_location, backedUp_salt=defaultBackedUp_salt_location, backedUp_database=defaultBackedUp_database_location):
    '''
    This function will restore previously backed up master password files and password database.
    '''

    restoreMasterlevelLocation = Path("Password_Manager/User/masterlevel")
    restoreMasterlevelLocation.mkdir(parents=True, exist_ok=True)

    restoreLeveldbLocation = Path("Password_Manager/User/leveldb")
    restoreLeveldbLocation.mkdir(parents=True, exist_ok=True)

    if os.path.exists(backedUp_key and backedUp_salt and backedUp_database):
        shutil.copy(backedUp_key,restoreMasterlevelLocation)
        shutil.copy(backedUp_salt,restoreMasterlevelLocation)
        shutil.copy(backedUp_database,restoreLeveldbLocation)
        print("\n[+] Restore Successful ✔ ✔ ✔")
    else:
        print("\n❌ Backup Configuration Not Found 📌\n")
    

def deleteLocalBackup():
    print('\n❌✌❌ deleting backup ❌✌❌')

    backedUp_folder = defaultBackupPath
    if os.path.exists(backedUp_folder):
        shutil.rmtree(backedUp_folder)

    with open("Password_Manager/config.json", "r+") as config_file:
        backupConfig = json.load(config_file)
        backupConfig['Automatic Backup'] = False
        config_file.seek(0)
        json.dump(backupConfig, config_file)
        config_file.truncate()
    print("\n[-] records deleted")