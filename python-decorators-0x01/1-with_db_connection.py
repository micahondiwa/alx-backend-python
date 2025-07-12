import sqlite3
import functools

def with_db_connection(func):
    pass

@with_db_connection
def get_user_by_db(conn, user_id):
    cursor  = conn.cursor()