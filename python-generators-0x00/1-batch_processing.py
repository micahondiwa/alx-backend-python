#!/usr/bin/python3

import mysql.connector

def stream_user_in_batches(batch_size):
    co