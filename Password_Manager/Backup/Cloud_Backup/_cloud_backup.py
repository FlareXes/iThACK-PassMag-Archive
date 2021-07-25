from Password_Manager.Backup.Cloud_Backup._cloud_db_manager import storePassword, storeEncryptionComponents,storeSecretEncryption
from Password_Manager.Backup.Cloud_Backup._cloud_user_db import connect_cloud_server
from Password_Manager.User._user_db import connect_database
import sqlite3
import json

def connect_local_database():
    connection = sqlite3.connect(r"Password_Manager/User/leveldb/user.db")
    return connection


def backup_Database_And_Config_On_Cloud():
    print("\n🐬🐬🐬 Backing Up On Cloud 🐬🐬🐬")
    
    sqlQuery_1 = "SELECT * FROM UserDataBase"
    connection = connect_local_database()
    mycursor = connection.cursor()
    entrysTuple = mycursor.execute(sqlQuery_1)
    for entry in entrysTuple:
        try:
            storePassword(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6])
        except:
            pass
    print("\n🎈 Cloud Backup First Stage Complete 🎈")

    sqlQuery_2 = "SELECT * FROM UserDataBase_Encryption"
    entrysTuple = mycursor.execute(sqlQuery_2)
    for entry in entrysTuple:
        try:
            storeEncryptionComponents(entry[0], entry[1])
        except:
            pass
    print("\n🤞🐬 Cloud Backup Second Stage Complete 🤞🐬")

    storeSecretEncryption()
    print("\n🐬🐬🐬 Cloud Backup Finished 🐬🐬🐬")

    connection.close()


def cloud_Restore():
    print("\n Please Wait This May Take Time")
    cloudConnection = connect_cloud_server()
    mycursor = cloudConnection.cursor()

    sqlQuery_1 = "SELECT * FROM UserDataBase"
    entryTuple_1 = mycursor.execute(sqlQuery_1)
    entryTuple_1 = mycursor.fetchall()

    sqlQuery_2 = "SELECT * FROM UserDataBase_Encryption"
    entryTuple_2 = mycursor.execute(sqlQuery_2)
    entryTuple_2 = mycursor.fetchall()

    # TODO: Commented Part Is Under R&D Department
    '''
    sqlQuery_3 = "SELECT * FROM Secret_Encryption"
    entryTuple_3 = mycursor.execute(sqlQuery_3)
    entryTuple_3 = mycursor.fetchall()
    print(entryTuple_3[0][1])
    print(entryTuple_3[0][2])

    with open("User/masterlevel/00003.1.KEY.bin", "w") as saltfile:
        saltfile.write(entryTuple_3[0][1])

    with open("User/masterlevel/00003.1.SALT.bin", "w") as saltfile:
        saltfile.write(entryTuple_3[0][2])
    '''

    cloudConnection.close()
    
    # ---------------- Local Work ----------------

    localConnection = connect_database()
    mycursor = localConnection.cursor()

    sqlQuery_1 = "INSERT OR IGNORE INTO UserDataBase (ID, Website, URL, Username, Email, Password, Description) VALUES (?, ?, ?, ?, ?, ?, ?)"
    mycursor.executemany(sqlQuery_1, entryTuple_1)

    sqlQuery_2 = "INSERT OR IGNORE INTO UserDataBase_Encryption (Identification, Encryption) VALUES (?, ?)" # https://stackoverflow.com/questions/12105198/sqlite-how-to-get-insert-or-ignore-to-work
    mycursor.executemany(sqlQuery_2, entryTuple_2)
    localConnection.commit()
    localConnection.close()
    print("\n🤞 Successfully Restored To The Previous Stage 🐬")


def deleteCloudBackup():
    print('\n❌✌❌ deleting cloud backup ❌✌❌')
    with open("Password_Manager/config.json", "r+") as config_file:
        isAutoBackupAllowed = json.load(config_file)
        isAutoBackupAllowed['Automatic Cloud Backup'] = False
        config_file.seek(0)
        json.dump(isAutoBackupAllowed, config_file)
        config_file.truncate()

    connection = connect_cloud_server()
    mycursor = connection.cursor()

    sqlQuery_1 = "DROP TABLE IF EXISTS UserDataBase"
    sqlQuery_2 = "DROP TABLE IF EXISTS UserDataBase_Encryption"
    sqlQuery_2 = "DROP TABLE IF EXISTS Secret_Encryption"

    mycursor.execute(sqlQuery_1)
    mycursor.execute(sqlQuery_2)
    mycursor.execute(sqlQuery_3)
    connection.commit()
    connection.close()
    print("\n[-] records deleted")