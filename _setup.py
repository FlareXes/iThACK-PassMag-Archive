from distutils.command.config import config
from Password_Manager.User._user_db import create_database
from Password_Manager.User._master_encryption import passwordHasher
import os
import json
import subprocess
import shutil

def warning():
    config_file = "Password_Manager/Config/config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as config_file:
            installation = json.load(config_file)['Installation']
    else:
        installation = False

    if installation:
        print("\n[-] It Seem Your Installation Is Already Done. If You Reinstall iThACK PassMag Then You Will Lost All Your Password.")
        choice = input("[+] Do You Still Wanna To Reinstall? (y/n): ")
        if choice == "n" or choice == "no":
            exit()
        elif choice == "y" or choice == "yes":
            remove_tree()
        else:
            print("\nInvalid Input. Process Canceled !")

def remove_tree():
    remove_trees = ("Password_Manager/User/leveldb", "Password_Manager/User/masterlevel")
    for location in remove_trees: shutil.rmtree(location, ignore_errors=True)

if __name__ == '__main__':
    warning()

    create_database()
    passwordHasher("don't use weak master password")

    data = {
        'Installation': True,
        'Automatic Backup': False,
        'Automatic Cloud Backup': False,
        'User Preferred Local Backup': False,
    }
    with open("Password_Manager/Config/config.json", "w") as config_file:
        json.dump(data, config_file)

    subprocess.check_call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])

    print("""    
 ____________________________________________
< Woo Hoo Installation Complete Successfully >
 --------------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\\
                ||------| \\
                ||     ||

    """)