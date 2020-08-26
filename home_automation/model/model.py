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

    def _exec(self, sql, values=''):
        conn = self._db_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        res = [dict(row) for row in cur.fetchall()]
        conn.close()

        return res
