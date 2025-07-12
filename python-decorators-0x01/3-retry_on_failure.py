import time
import sqlite3
import functools

@with_db_connection
@retry_on_failure(retry=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()