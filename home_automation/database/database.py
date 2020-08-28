import sqlite3
from sqlite3 import Error
from pathlib import Path

from home_automation.settings import DB_PATH


def _get_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def _create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def _create_lights(conn):
    sql_create_ligths = """ CREATE TABLE IF NOT EXISTS lights (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status integer default 0,
                                creation_date text
                            ); """
    _create_table(conn, sql_create_ligths)


def _create_thermostats(conn):
    sql_create_thermostats = """CREATE TABLE IF NOT EXISTS thermostats (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    temp integer default 0,
                                    creation_date text
                                );"""
    _create_table(conn, sql_create_thermostats)


def create_database():
    db = Path(f'{DB_PATH}/database.db')
    if not db.exists:
        conn = _get_connection(DB_PATH)

        _create_lights(conn)
        _create_thermostats(conn)

        conn.close()


if __name__ == "__main__":
    create_database()
