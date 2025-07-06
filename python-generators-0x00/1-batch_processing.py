#!/usr/bin/python3

import mysql.connector

def stream_user_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Admin@123',
        database='ALX_prodev'
    )