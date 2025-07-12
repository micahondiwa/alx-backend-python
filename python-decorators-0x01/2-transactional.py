import sqlite3
import functools

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ? ", (new_email, user_id))

#### Update user's email with automatic transaction handling 
