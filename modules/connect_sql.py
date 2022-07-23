import os
import sqlite3

conn = sqlite3.connect(os.path.join("db", "data.db"))
cursor = conn.cursor()


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


def db_not_exists():  # sourcery skip: use-named-expression
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='farms_id'"
    )
    table_exists = cursor.fetchall()
    if table_exists:
        return False
    return True
