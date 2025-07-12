import time
import sqlite3
import functools

query_cache = {}

@with_db_connection
@cache_query 
def fecth_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()