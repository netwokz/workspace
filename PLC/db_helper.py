from contextlib import closing
import sqlite3
import os
import pandas as pd


class WODBHelper:

    DB_PATH = ""
    TABLE_NAME = "my_table"

    def __init__(self, db_location: str):
        self.DB_PATH = db_location
        self.check_db()

    def init_db(self) -> None:
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS my_table (wo_id TEXT, desc TEXT, type TEXT, owner TEXT, max TEXT, link TEXT)")
                return False

    def check_db(self) -> bool:
        return os.path.exists(self.DB_PATH)

    def does_table_exist(self):
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='my_table' ''')
                # if the count is 1, then table exists
                if cursor.fetchone()[0] == 1:
                    # Table exists
                    return True
                else:
                    # Table does not exist.
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS my_table (name TEXT, entry TEXT, time TEXT)")
                    return False

    def add_entry(self, wo_id, desc, type, owner, max, link):
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "INSERT INTO my_table (wo_id, desc, type, owner, max, link) VALUES (?,?,?,?,?,?)", (wo_id, desc, type, owner, max, link))
                conn.commit()

    def get_entries(self):
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            data = pd.read_sql_query("SELECT * FROM my_table", conn)
            return data

    def has_entry(self, wo_id) -> bool:
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                rows = cursor.execute(
                    "SELECT wo_id FROM my_table WHERE wo_id = ?", (wo_id,)).fetchall()
                if rows:
                    return True
                else:
                    return False

    def delete_entry(self, wo_id):
        with closing(sqlite3.connect(self.DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "DELETE FROM my_table WHERE wo_id = ?", (wo_id,))
                conn.commit()

    def delete_db(self):
        os.remove(self.DB_PATH)
