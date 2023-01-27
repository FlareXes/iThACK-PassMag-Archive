import sqlite3
from typing import List, Tuple

from iThACK import DATABASE
from iThACK.template import Account, CipherConfig
from iThACK.utils import attrs


class Database:
    def __init__(self, account: Account = None, cipher_config: CipherConfig = None):
        if account is None and cipher_config is None:
            self.conn = sqlite3.connect(DATABASE)
            self.cursor = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(DATABASE)
            self.cursor = self.conn.cursor()
            self.account = account
            self.cipher_config = cipher_config

        self.cursor.execute("PRAGMA foreign_keys=ON")

    def __del__(self):
        self.conn.close()

    def init_database(self):
        account_table_schema = """
        CREATE TABLE IF NOT EXISTS Accounts
        (id              INTEGER     PRIMARY KEY,
         site            TEXT        NOT NULL,
         username        TEXT        NOT NULL,
         url             TEXT        NOT NULL);
        """

        self.cursor.execute(account_table_schema)
        self.conn.commit()

        encryption_table_schema = """
        CREATE TABLE IF NOT EXISTS CipherStuff
        (accountId       INTEGER       PRIMARY KEY,
         ciphertext      TEXT          NOT NULL,
         salt            TEXT          NOT NULL,
         tag             TEXT          NOT NULL,
         nonce           TEXT          NOT NULL,
         FOREIGN KEY(accountID) REFERENCES Accounts(id) ON DELETE CASCADE);
        """

        self.cursor.execute(encryption_table_schema)
        self.conn.commit()

    def read(self, *columns, accounts: bool = True, cc: bool = False, full: bool = False) -> List[Tuple]:
        columns = ", ".join(columns)

        if columns != "":
            query = f"SELECT {columns} FROM Accounts JOIN CipherStuff ON Accounts.id=CipherStuff.accountId;"
        else:
            if full:
                query = """
                SELECT id, site, username, url, ciphertext, salt, tag, nonce FROM Accounts
                JOIN CipherStuff ON Accounts.id=CipherStuff.accountId;
                """

            if accounts:
                query = "SELECT * FROM Accounts"

            if cc:
                query = "SELECT * FROM CipherStuff"

        self.cursor.execute(query)
        res = self.cursor.fetchall()

        return res

    def create(self):
        account_query = """
        INSERT INTO Accounts (
        site, username, url
        ) VALUES (?, ?, ?)
        """

        cipher_query = """
        INSERT INTO CipherStuff (
        accountId, ciphertext, salt, tag, nonce
        ) VALUES (?, ?, ?, ?, ?)
        """

        self.cursor.execute(account_query, attrs(self.account)[1:])
        last_id = (self.cursor.lastrowid,)
        self.cursor.execute(cipher_query, last_id + attrs(self.cipher_config))
        self.conn.commit()

    def delete(self) -> None:
        account_query = "DELETE FROM Accounts WHERE id = ?"
        self.cursor.execute(account_query, (self.account.acc_id,))
        self.conn.commit()


class Filter:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def select(self, _id: int) -> Tuple[Account, CipherConfig]:
        account_query = "SELECT * FROM Accounts WHERE id = ?"
        self.cursor.execute(account_query, (_id,))
        account = self.cursor.fetchone()

        cipher_query = "SELECT * FROM CipherStuff WHERE accountId = ?"
        self.cursor.execute(cipher_query, (_id,))
        cipher = self.cursor.fetchone()

        return Account(*account), CipherConfig(*cipher[1:])
