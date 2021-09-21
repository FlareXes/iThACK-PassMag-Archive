import mysql.connector
import json
import os


with open("Password_Manager\Config\cloud_cred.json", "r") as CloudCred:
    CLEVER_CLOUD = json.load(CloudCred)["CleverCloud"]

MYSQL_ADDON_DB = CLEVER_CLOUD["MYSQL_ADDON_DB"]
MYSQL_ADDON_HOST = CLEVER_CLOUD["MYSQL_ADDON_HOST"]
MYSQL_ADDON_PASSWORD = CLEVER_CLOUD["MYSQL_ADDON_PASSWORD"]
MYSQL_ADDON_USER = CLEVER_CLOUD["MYSQL_ADDON_USER"]


def connect_cloud_server():
    '''
    Get connection to the cloud server.
    '''
    connection = mysql.connector.connect(user=MYSQL_ADDON_USER, password=MYSQL_ADDON_PASSWORD, host=MYSQL_ADDON_HOST, database=MYSQL_ADDON_DB)
    return connection


def create_dbtables():
    '''
    Create tables on the database.
    '''
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