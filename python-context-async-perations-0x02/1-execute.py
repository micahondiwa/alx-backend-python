import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params if params is not None else ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Return False to propagate any exceptions
        return False

# Using the context manager with our specific query
with ExecuteQuery(
    query="SELECT * FROM users WHERE age > ?",
    params=(25,)
) as results:
    print("Users over 25 years old:")
    for row in results:
        print(row)
        