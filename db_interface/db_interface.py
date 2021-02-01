import mysql.connector as conn
from mysql.connector import Error
from config.config import config

MYSQL = config('MYSQL')


def open_conn(db=None, cursor=None):
    try:
        if db is None:
            db = conn.connect(
                host=MYSQL['HOST'],
                user=MYSQL['USER'],
                passwd=MYSQL['PASSWD'],
                database=MYSQL['DATABASE']
            )

        if db.is_connected():
            print(f"Connected to {MYSQL['DATABASE']}.")

        if cursor is None:
            cursor = db.cursor()

    except Error as e:
        print(e)

    return db, cursor


def close_conn(db, cursor):
    if db is not None and db.is_connected():
        db.close()
        cursor.close()
