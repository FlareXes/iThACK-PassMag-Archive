import json
from os import listdir
from tkinter import Tk
from tkinter.filedialog import askdirectory
from Password_Manager.Backup.Local_Backup._local_backup import backup_Database_And_Config, restore

Tk().withdraw()

def preferredLocalBackup():
    filename = askdirectory(title='Export iThACK PassMag Backup') + '/iThACK PassMag'
    backup_Database_And_Config(backupPath=filename)
    
    with open("Password_Manager/Config/config.json", "r+") as config_file:
        backupConfig = json.load(config_file)
        backupConfig['User Preferred Local Backup'] = True
        config_file.seek(0)
        json.dump(backupConfig, config_file)
        config_file.truncate()

def preferredLocalRestore():
    dirname = askdirectory(title='Open iThACK PassMag Backup')
    files = listdir(dirname)
    if files == ['00003.1.KEY.bin', '00003.1.SALT.bin', 'user.db']:
        backedUp_key = dirname + "/00003.1.KEY.bin"
        backedUp_salt = dirname + "/00003.1.SALT.bin"
        backedUp_database = dirname + "/user.db"
        restore(backedUp_key, backedUp_salt, backedUp_database)
    else:
        print('\n❌❌❌ Backup Folder Should Only Consist iThACK PassMag Files ❌❌❌')