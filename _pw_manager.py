from Password_Manager._pwmag_menu import menu, backupMenu, addEntry, deleteEntry, changeMasterPassword, showPassword, backup, cloudBackup, exportEntriesCsv, showEntries
from Password_Manager.Backup.Local_Backup._local_backup import restore
from Password_Manager.Backup.Cloud_Backup._cloud_backup import cloud_Restore
from Password_Manager._Authenticate import checkTrust
from Password_Manager._config_checkup import checkConfigurations
import json

if __name__ == '__main__':
    cloud_Restore()
    checkConfigurations()
    checkTrust()

while True:
    choice = menu()

    if choice == '1':
        showPassword()
    elif choice == '2':
        addEntry()
    elif choice == '3':
        deleteEntry()
    elif choice == '4':
        showEntries()
    elif choice == '5':
        changeMasterPassword()
    elif choice == '6':
        print("\n----------------------------------------------------------------")
        options = backupMenu()
        if options == '1':
            backup() 
            print("\n👌 All Password Has Been Backed Up On Local System 📌")
            print("\n👌 From Next Time All Passwords Automaticly Will Be Backed Up 📌")
        elif options == '2':
            cloudBackup()
            print("\n👌 All Password Has Been Backed Up On Cloud 📌")
            print("\n👌 From Next Time All Passwords Automaticly Will Be Backed Up 📌")
        elif options == '4':
            restore("masterpassword")
            restore("passworddatabase")
            print("\n🤞 Successfully Restored To The Previous Stage 🐬")
        elif choice == 'Q' or choice == 'q':
            exit()
        else:
            pass
    elif choice == '7':
        exportEntriesCsv()
    elif choice == 'Q' or choice == 'q':
        exit()
    else:
        pass