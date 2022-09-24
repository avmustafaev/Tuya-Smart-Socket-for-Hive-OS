import os
import sqlite3


conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


def backup_db():
    conn_back = sqlite3.connect(os.path.join("db", "data.db"))
    conn.backup(conn_back)
    conn.commit()
    conn_back.commit()
    # conn.close()
    conn_back.close()


def sql_zapros(sql_string, tupple):
    cursor.execute(sql_string, tupple)
    response_list = cursor.fetchall()
    conn.commit()
    return response_list


def init_db():
    """Инициализирует БД"""
    with open(os.path.join("install", "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def db_not_exists():    # sourcery skip: use-named-expression
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='farms_id'"
    )
    table_exists = cursor.fetchall()
    return not table_exists
