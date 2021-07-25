from Password_Manager._pwmag_menu import menu, backupMenu, addEntry, deleteEntry, changeMasterPassword, showPassword,\
     backup, cloudBackup, exportEntriesCsv, showEntries, checkPwnedPasswords, stopCloudBackup, stopLocalBackup, \
         restoreLocalBackup, importCsv, userPreferredBackup, userPreferredRestore
from Password_Manager.Backup.Cloud_Backup._cloud_backup import cloud_Restore
from Password_Manager._Authenticate import checkTrust
from Password_Manager._config_checkup import checkConfigurations


if __name__ == '__main__':
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
        elif options == '2':
            restoreLocalBackup()
        elif options == '3':
            stopLocalBackup()
        elif options == '4':
            cloudBackup()
        elif options == '5':
            cloud_Restore()
        elif options == '6':
            stopCloudBackup()
        elif options == '7':
            userPreferredBackup()
        elif options == '8':
            userPreferredRestore()
        elif choice == 'Q' or choice == 'q':
            exit()
        else:
            pass
        
    elif choice == '7':
        exportEntriesCsv()
    elif choice == '8':
        importCsv()
    elif choice == '9':
        checkPwnedPasswords()
    elif choice == 'Q' or choice == 'q':
        exit()
    else:
        pass