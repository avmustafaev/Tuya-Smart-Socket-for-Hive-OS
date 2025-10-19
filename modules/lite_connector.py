import os
import sqlite3


class LiteConnector:
    def __init__(self):
        #self.conn = sqlite3.connect(":memory:")
        self.conn = sqlite3.connect(os.path.join("db", "data.db"))
        self.cursor = self.conn.cursor()
        if self.db_not_exists():
            self.init_db()

    def db_not_exists(self):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='farms_id'"
        )
        table_exists = self.cursor.fetchall()
        return not table_exists

    def init_db(self):
        with open(os.path.join("install", "createdb.sql"), "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()

    def backup_db(self):
        self.conn_back = sqlite3.connect(os.path.join("db", "data_bk.db"))
        self.conn.backup(self.conn_back)
        self.conn.commit()
        self.conn_back.commit()
        self.conn_back.close()

    def request(self, sql_string, tupple):
        self.cursor.execute(sql_string, tupple)
        response_list = self.cursor.fetchall()
        self.conn.commit()
        return response_list
