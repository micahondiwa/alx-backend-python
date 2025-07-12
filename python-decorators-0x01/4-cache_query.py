import time
import sqlite3
import functools

query_cache = {}

def cache_query(func):
    @wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = query

        if cache_key in query_cache:
            print("Cached result")
            return query_cache[cache_key]
@with_db_connection
@cache_query 
def fecth_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fecth_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fecth_users_with_cache(query="SELECT * FROM users")