import sqlite3
from typing import List, Tuple

from iThACK.database import DATABASE


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def init_database(self):
        table_schema = """
        CREATE TABLE IF NOT EXISTS accounts
        (id              INTEGER          PRIMARY KEY,
         site            TEXT(50)         NOT NULL,
         username        TEXT(200)        NOT NULL,
         url             TEXT(500)        NOT NULL);
        """

        self.cursor.execute(table_schema)
        self.conn.commit()

    def insert(self, account):
        query = """
        INSERT INTO accounts (
        id, site, username, url
        ) VALUES (?, ?, ?, ?)
        """

        self.cursor.execute(query, account.get())
        self.conn.commit()

    def read(self) -> List[Tuple]:
        query = "SELECT * FROM accounts"
        self.cursor.execute(query)
        accounts = self.cursor.fetchall()
        return accounts
