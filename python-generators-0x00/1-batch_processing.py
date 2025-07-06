#!/usr/bin/python3

import mysql.connector

def streamusersinbatches(batchsize):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Admin@123',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batchsize)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()

def batch_processing(batchsize):
    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                print(user)