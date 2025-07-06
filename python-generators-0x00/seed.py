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
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX(user_id) 
        );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")