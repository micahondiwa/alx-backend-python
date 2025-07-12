import sqlite3
import functools

#### decorator to log SQL queries 
def log_queries():
    pass

@log_queries 
def fetch_all_users(query):
    conn =  sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()