import mysql.connector
import csv
from mysql.connector import errorcode

# 1. Connect to MySQL Server (no DB selected yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',      # Use IP for compatibility
            port=3306,
            user='root',
            password='Admi@n123'     # <<< change this to your real root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Server: {err}")
        return None

# 2. Create database if not exists
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
        print("Database created (or already exists).")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

# 3. Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Admin@123',   # <<< same password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev DB: {err}")
        return None

# 4. Create the user_data table
def create_table(connection):
    create_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 2) NOT NULL,
        INDEX(user_id)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_query)
        connection.commit()
        cursor.close()
        print("Table user_data created (or already exists).")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")

# 5. Insert data from CSV
def insert_data(connection, filename):
    try:
        cursor = connection.cursor()
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if record already exists by user_id
                check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (row['user_id'],))
                if not cursor.fetchone():
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
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# 6. Optional generator to stream data row-by-row
def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
