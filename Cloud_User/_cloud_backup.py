import sqlite3
from Cloud_User._cloud_db_manager import storePassword, storeEncryptionComponents,storeSecretEncryption

def connect_local_database():
    connection = sqlite3.connect(r"User/leveldb/user.db")
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