import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
    

@with_db_connection
def get_user_by_db(conn, user_id):
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id= ?", (user_id,))
    return cursor.fetchone()

#### Fetch user ID with automatic connection handling
user = get_user_by_db(user_id=1)
print(user)