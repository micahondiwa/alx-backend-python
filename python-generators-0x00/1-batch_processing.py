#!/usr/bin/python3

import mysql.connector

def stream_user_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Admin@123',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()