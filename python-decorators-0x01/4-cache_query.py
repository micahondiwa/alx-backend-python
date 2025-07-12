import time
import sqlite3
import functools

query_cache = {}

@with_db_connection
@cache_query 
