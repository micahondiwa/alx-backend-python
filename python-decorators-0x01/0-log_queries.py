import sqlite3
import functools

#### decorator to log SQL queries 
def log_queries():
    @functools.wraps(func)
    def wrapper(*args, **Kwargs):
        query = Kwargs.get('query')
        if not query and len(args) > 0:
            query = args[0]
        return func(*args, **Kwargs)
    return wrapper

@log_queries 
def fetch_all_users(query):
    conn =  sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")