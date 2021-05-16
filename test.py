from User._user_db import connect_database
from prettytable import PrettyTable
from User._data_encryption import encryptPassword, decryptPassword
import pandas as pd

def showWebsites():
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
        encryptionComponents = rows_1[i][5]+str(rows_2[i][0])
        cipher_text = encryptionComponents[:-168]
        salt = encryptionComponents[-168:-48]
        nonce = encryptionComponents[-48:-24]
        tag = encryptionComponents[-24:]
        decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, "plz").decode('utf-8')
        rowList = list(rows_1[i])
        rowList[5] = decryptedPassword
        ExportEntries.append(tuple(rowList))


    df = pd.DataFrame(ExportEntries, columns=["ID", "Website", "URL", "Username", "Email", "Password", "Description"])
    df.to_csv("thisis.csv", index=False)

showWebsites()