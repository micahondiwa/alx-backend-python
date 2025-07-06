#!/usr/bin/python3

import mysql.connector
import csv
import uuid
from mysql.connector import errorcode 

def connect_db():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="rot",
            password="Admin@123" 
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
            host='127.0.0.1',
            user='root',
            password='Admin@123',
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

def insert_data(connection, filename):
    try:
        cursor=connection.cursor()
        with open(filename, newline='') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (row['user_id'], ))
                if not cursor.fetchnone():
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        row['user_id'],
                        row['name'],
                        row['email'],
                        row['age']
                    ))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")

def stream_users(connection):
    cursor=connection.cursor(disctionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
