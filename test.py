from Cloud_User._cloud_user_db import connect_cloud_server
from User._user_db import connect_database

def cloud_Restore():
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

cloud_Restore()