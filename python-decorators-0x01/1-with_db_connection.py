import sqlite3
import functools

def with_db_connection(func):
    pass

@with_db_connection
def get_user_by_db(conn, user_id):
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id= ?", (user_id,))
    return cursor.fetchone()

#### Fetch user ID with automatic connection handling