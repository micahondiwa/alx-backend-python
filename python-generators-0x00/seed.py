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
        