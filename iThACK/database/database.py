import sqlite3
from functools import singledispatchmethod
from typing import List, Tuple

from iThACK.database import DATABASE
from iThACK.template import Account
from iThACK.utils import attrs


class Database:
    @singledispatchmethod
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    @__init__.register(Account)
    def _from(self, account):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()
        self.account = account

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

    def create(self):
        query = """
        INSERT INTO accounts (
        site, username, url
        ) VALUES (?, ?, ?)
        """

        self.cursor.execute(query, attrs(self.account)[1:])
        self.conn.commit()

    def read(self) -> List[Tuple]:
        query = "SELECT * FROM accounts"
        self.cursor.execute(query)
        accounts = self.cursor.fetchall()
        return accounts

    def delete(self) -> None:
        query = "DELETE FROM accounts WHERE id = ?"
        self.cursor.execute(query, (self.account.acc_id,))
        self.conn.commit()
