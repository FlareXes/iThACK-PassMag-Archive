from Cloud_User._cloud_user_db import connect_cloud_server


def storePassword(id, web_name, url, username, email, password, description):
    sqlQuery = "INSERT IGNORE INTO UserDataBase (ID, Website, URL, Username, Email, Password, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id, web_name, url, username, email, password, description)
    
    connection = connect_cloud_server()
    mycursor = connection.cursor()
    mycursor.execute(sqlQuery, val)
    connection.commit()
    connection.close()


def storeEncryptionComponents(entryID, encryptionComponents):
    sqlQuery = "INSERT IGNORE INTO UserDataBase_Encryption (Identification, Encryption) VALUES (%s, %s)"
    val = (entryID, encryptionComponents)

    connection = connect_cloud_server()
    mycursor = connection.cursor()
    mycursor.execute(sqlQuery, val)
    connection.commit()
    connection.close()


def storeSecretEncryption():
    with open("User/masterlevel/00003.1.KEY.bin", "rb") as keyFile:
        key = str(keyFile.read())
    with open("User/masterlevel/00003.1.SALT.bin", "rb") as saltFile:
        salt = str(saltFile.read())

    sqlQuery = "INSERT IGNORE INTO Secret_Encryption (Identification, KeyFile, SaltFile) VALUES (%s ,%s, %s)"
    val = (1, key, salt)

    connection = connect_cloud_server()
    mycursor = connection.cursor()
    mycursor.execute(sqlQuery, val)
    connection.commit()
    connection.close()


# https://www.tutorialspoint.com/mysql/mysql-handling-duplicates.htm