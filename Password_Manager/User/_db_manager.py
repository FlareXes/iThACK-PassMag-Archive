from Password_Manager.User._user_db import connect_database
from prettytable import PrettyTable
from Password_Manager.User._data_encryption import encryptPassword, decryptPassword
import pandas as pd


def storePassword(web_name, url, username, email, password, description):
    sqlQuery = "INSERT INTO UserDataBase (Website, URL, Username, Email, Password, Description) VALUES (?, ?, ?, ?, ?, ?)"
    val = (web_name, url, username, email, password, description)
    connection = connect_database()

    mycursor = connection.cursor()
    mycursor.execute(sqlQuery, val)
    connection.commit()
    connection.close()
    print("\n[+] record inserted.")

    last_entry_id = mycursor.lastrowid
    return last_entry_id


def deletePassword(acc_Id):
    connection = connect_database()
    mycursor = connection.cursor()

    sqlQuery_1 = "DELETE FROM UserDataBase WHERE Id = ?"
    sqlQuery_2 = "DELETE FROM UserDataBase_Encryption WHERE Identification = ?"
    accIdToDelete = (acc_Id,)

    mycursor.execute(sqlQuery_1, accIdToDelete)
    mycursor.execute(sqlQuery_2, accIdToDelete)
    connection.commit()
    connection.close()
    print("\n[-] record deleted")

def showWebsites():
    sqlQuery = "SELECT ID, Website, URL, Username, Email, Description FROM UserDataBase"

    connection = connect_database()
    mycursor = connection.cursor()
    mycursor.execute(sqlQuery)
    rows = mycursor.fetchall()
    connection.close()

    myTable = PrettyTable(["ID", "Website", "URL", "Username", "Email", "Description"])
    # Adding Data To Columns
    for row in rows:
        row = list(row)
        myTable.add_row(row)
    print(myTable)
    return len(rows)


def getPasswordComponents(acc_Id):
    connection = connect_database()
    mycursor = connection.cursor()

    sqlQuery_1 = "SELECT Password FROM UserDataBase WHERE Id = ?"
    sqlQuery_2 = "SELECT Encryption FROM UserDataBase_Encryption WHERE Identification = ?"
    entryID = (acc_Id,)

    mycursor.execute(sqlQuery_1, entryID)
    for cipher_text in mycursor.fetchone():
        cipher_text = cipher_text

    mycursor.execute(sqlQuery_2, entryID)
    for encryptionComponents in mycursor.fetchone():
        encryptionComponents = encryptionComponents

    return cipher_text + encryptionComponents


def storeEncryptionComponents(entryID, encryptionComponents):
    sqlQuery = "INSERT INTO UserDataBase_Encryption (Identification, Encryption) VALUES (?, ?)"
    val = (entryID, encryptionComponents)

    connection = connect_database()
    mycursor = connection.cursor()
    mycursor.execute(sqlQuery, val)
    connection.commit()
    connection.close()


def updateDatabaseWithNewMasterPassword(masterPassword, newMasterPassword):
    connection = connect_database()
    mycursor = connection.cursor()

    sqlQuery_1 = "SELECT DISTINCT ID, Password FROM 'UserDataBase' WHERE ID IN (SELECT DISTINCT Identification FROM UserDataBase_Encryption)"
    mycursor.execute(sqlQuery_1, )
    IDPassword = mycursor.fetchall()

    sqlQuery_2 = "SELECT DISTINCT Identification, Encryption FROM 'UserDataBase_Encryption' WHERE Identification IN (SELECT DISTINCT ID FROM UserDataBase)"
    mycursor.execute(sqlQuery_2, )
    IDEncryptionComponent = mycursor.fetchall()

    for IDPasswordTuple, IDEncryptionComponentTuple in zip(IDPassword, IDEncryptionComponent):
        entryID = IDPasswordTuple[0]
        cipher_text = IDPasswordTuple[1]
        encryptionComponents = IDEncryptionComponentTuple[1]

        salt = encryptionComponents[-168:-48]
        nonce = encryptionComponents[-48:-24]
        tag = encryptionComponents[-24:]

        decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, masterPassword).decode('utf-8')

        newPasswordEncryptionComponents = encryptPassword(decryptedPassword, newMasterPassword)
        salt = newPasswordEncryptionComponents['salt']
        nonce = newPasswordEncryptionComponents['nonce']
        tag = newPasswordEncryptionComponents['tag']
        password = newPasswordEncryptionComponents['cipher_text']

        sqlQuery = "UPDATE UserDataBase SET Password = ? WHERE ID = ?"
        val = (password, entryID)
        mycursor.execute(sqlQuery, val)
        connection.commit()

        sqlQuery = "UPDATE UserDataBase_Encryption SET Encryption = ? WHERE Identification = ?"
        val = (salt + nonce + tag, entryID)
        mycursor.execute(sqlQuery, val)
        connection.commit()

    connection.close()


def exportPasswords():
    connection = connect_database()
    mycursor = connection.cursor()
    sqlQuery_1 = "SELECT ID, Website, URL, Username, Email, Password, Description FROM UserDataBase"
    mycursor.execute(sqlQuery_1)
    rows_1 = mycursor.fetchall()

    sqlQuery_2 = "SELECT Encryption FROM UserDataBase_Encryption"
    mycursor.execute(sqlQuery_2)
    rows_2 = mycursor.fetchall()

    ExportEntries = []
    for i in range(0, len(rows_2)):
        encryptionComponents = rows_1[i][5] + str(rows_2[i][0])
        cipher_text = encryptionComponents[:-168]
        salt = encryptionComponents[-168:-48]
        nonce = encryptionComponents[-48:-24]
        tag = encryptionComponents[-24:]
        decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, "plz").decode('utf-8')
        rowList = list(rows_1[i])
        rowList[5] = decryptedPassword
        ExportEntries.append(tuple(rowList))

    df = pd.DataFrame(ExportEntries, columns=["ID", "Website", "URL", "Username", "Email", "Password", "Description"])
    df.to_csv("export.csv", index=False)
    connection.close()

def getColumn(columnName):
    columnName = columnName.split(' ')[0]
    connection = connect_database()
    mycursor = connection.cursor()

    sqlQuery = f"SELECT ID, {columnName} FROM UserDataBase"
    mycursor.execute(sqlQuery)
    rows_1 = mycursor.fetchall()
    connection.close()

    columnEnties = []
    for columnEntry in rows_1:
        columnEnties.append(columnEntry)

    return columnEnties