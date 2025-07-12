import time
import sqlite3
import functools

query_cache = {}
def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    @wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception e:
            conn.rollback()
            raise e
        
def cache_query(func):
    @wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = query

        if cache_key in query_cache:
            print("Cached result")
            return query_cache[cache_key]
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        print("Caching new result")
        return result
    return wrapper 
 
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