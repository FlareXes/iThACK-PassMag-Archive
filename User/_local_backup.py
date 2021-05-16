import shutil
from pathlib import Path
import glob
import os

def backup_Database_And_Config():
    # create path, if it doesn't exist'
    location = Path("C:\\ProgramData\\iThACK PassMag")
    location.mkdir(parents=True, exist_ok=True)
    
    # copy database from leveldb
    shutil.copy("User/leveldb/user.db", location)
    
    # copy all file from masterlevel
    files_to_backup = glob.glob("User/masterlevel/*.bin")
    for filename in files_to_backup:
        shutil.copy(filename, location)


def restore(whatToBackup):
    if whatToBackup == "masterpassword":
        backedUp_key = "C:\\ProgramData\\iThACK Passmag\\00003.1.KEY.bin"
        backedUp_salt = "C:\\ProgramData\\iThACK Passmag\\00003.1.SALT.bin"

        restoreFileLocation = Path("User/masterlevel")
        restoreFileLocation.mkdir(parents=True, exist_ok=True)

        if os.path.exists(backedUp_key and backedUp_salt):
            shutil.copy(backedUp_key,restoreFileLocation)
            shutil.copy(backedUp_salt,restoreFileLocation)
        else:
            print("\n❌ Backup Configuration Not Found 📌\n")
            exit()

    elif whatToBackup == "passworddatabase":
        backedUp_database = "C:\\ProgramData\\iThACK Passmag\\user.db"

        restoreFileLocation = Path("User/leveldb")
        restoreFileLocation.mkdir(parents=True, exist_ok=True)

        if os.path.exists(backedUp_database):
            shutil.copy(backedUp_database,restoreFileLocation)
        else:
            print("\n❌ Backup Configuration Not Found 📌\n")
            exit()