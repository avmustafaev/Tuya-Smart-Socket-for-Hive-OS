import os
import sqlite3


class LiteConnector:
    def __init__(self, db_path=":memory:", backup_path="db/data_bk.db"):
        """
        Инициализирует соединение с SQLite базой данных.
        
        :param db_path: Путь к основной базе данных (по умолчанию в памяти)
        :param backup_path: Путь к резервной копии
        """
        self.db_path = db_path
        self.backup_path = backup_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if not self.check_table_exists("farms_id"):
            self.init_db()

    def check_table_exists(self, table_name):
        """
        Проверяет существование таблицы в базе данных.
        
        :param table_name: Имя таблицы для проверки
        :return: True, если таблица существует, иначе False
        """
        self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}' LIMIT 1"
        )
        return bool(self.cursor.fetchone())

    def init_db(self):
        """
        Инициализирует базу данных из SQL-скрипта.
        """
        sql_script_path = os.path.join("install", "createdb.sql")
        if not os.path.exists(sql_script_path):
            raise FileNotFoundError(f"SQL-скрипт не найден: {sql_script_path}")
        
        with open(sql_script_path, "r") as f:
            sql = f.read()
        
        self.cursor.executescript(sql)
        self.conn.commit()

    def backup_db(self):
        """
        Создает резервную копию базы данных.
        """
        # Убедимся, что директория для резервной копии существует
        os.makedirs(os.path.dirname(self.backup_path), exist_ok=True)
        
        with sqlite3.connect(self.backup_path) as conn_back:
            self.conn.backup(conn_back)
            conn_back.commit()  # Только резервная копия требует коммита

    def request(self, sql_string, params=None):
        """
        Выполняет SQL-запрос и возвращает результаты.
        
        :param sql_string: SQL-запрос
        :param params: Параметры для запроса (tuple или dict)
        :return: Результаты запроса (list)
        """
        if params is None:
            self.cursor.execute(sql_string)
        else:
            self.cursor.execute(sql_string, params)
        
        # Возвращаем результаты только если запрос SELECT
        if sql_string.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        self.conn.commit()
        return []
