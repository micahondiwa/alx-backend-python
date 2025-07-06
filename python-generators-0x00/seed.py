#!/usr/bin/python3

import mysql.connector
import csv
import uuid
from mysql.connector import errorcode 

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="rot",
            password=" "
        )
    except mysql.connector.Error as err:
        print(f"Error conncting: {err}")
        return None

def create_database(connection):
    try:
        cursor=connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password=' ',
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    query="""

    """