import mysql.connector
import os

def connect_cloud_server():
    connection = mysql.connector.connect(user="ukjqcvpzl1zyir4e", password="9GwcPYLnFmbynDP43nfg", host="bzgvile1yxwbntvbgrnu-mysql.services.clever-cloud.com", database="bzgvile1yxwbntvbgrnu")
    # print(connection)
    return connection


def create_dbtables():
    conn = connect_cloud_server()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS UserDataBase
         (ID                INTEGER          PRIMARY KEY,
         Website            CHAR(50)         Null,
         URL                TEXT(500)        NOT NULL,
         Username           CHAR(50)         NULL,
         Email              CHAR(50)         NOT NULL,
         Password           TEXT(200)        NOT NULL,
         Description        TEXT(5000));''')


    cur.execute('''CREATE TABLE IF NOT EXISTS UserDataBase_Encryption
         (Identification    INTEGER         Not Null,
          Encryption        CHAR(255)       Not Null);''')
    

    cur.execute('''CREATE TABLE IF NOT EXISTS Secret_Encryption
         (Identification    INTEGER          PRIMARY KEY,
          KeyFile           TEXT(1000)       Not Null,
          SaltFile          TEXT(1000)       Not Null);''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_dbtables()