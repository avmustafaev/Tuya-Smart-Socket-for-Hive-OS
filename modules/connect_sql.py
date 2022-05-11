import os
import sqlite3

conn = sqlite3.connect(os.path.join("db", "data.db"))
cursor = conn.cursor()

def sql_zapros(sql_string, tupple):
    # connection = sqlite3.connect('smartsocket.db')
    # cursor = connection.cursor()
    cursor.execute(sql_string, tupple)
    response_list = cursor.fetchall()
    conn.commit()
    # connection.close()
    return response_list


def _init_db():
    """Инициализирует БД"""
    with open(os.path.join("install", "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='farms_id'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()