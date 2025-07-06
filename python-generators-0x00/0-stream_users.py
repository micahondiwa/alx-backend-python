#!/usr/bin/python3

import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Admin@123',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row 
    
    cursor.close
    connection.close()