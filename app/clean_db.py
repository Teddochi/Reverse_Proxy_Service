#!/usr/bin/env python
# encoding: utf-8

import constants
import mysql.connector
            
# Connect to MySQL database
db = mysql.connector.connect(**constants.MYSQL_CONNECT_INFO)
cursor = db.cursor()

# Clean the queries and slow_requests tables
cursor.execute(constants.CLEAN_QUERIES_COMMAND)
cursor.execute(constants.CLEAN_SLOW_REQUESTS_COMMAND)
db.commit()

cursor.close()
db.close()