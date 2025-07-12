import sqlite3
import functools

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    