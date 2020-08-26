import sqlite3
from sqlite3 import Error

from home_automation.settings import DB_PATH


class Model():
    def _db_conn(self):
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH)
        except Error as e:
            # logging here
            print(e)
            pass

        return conn

    def _exec(self, sql):
        pass
