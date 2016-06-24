#!/usr/bin/python
# version.py – Fetch and display the MySQL database server version.

# import the MySQLdb and sys modules
import MySQLdb
import sys
from announcement import Announcement

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
connection = MySQLdb.connect(host="192.168.23.3", user="streamin_upload", passwd="upload88", db="streamin_equities")

# prepare a cursor object using cursor() method
cursor = connection.cursor()

# execute the SQL query using execute() method.
cursor.execute("Select * from company_announcements where link ='01106368'")

# fetch a single row using fetchone() method.
row = cursor.fetchone()
for row in cursor:
    print(row)
    test_announce = Announcement(*row)
    print(test_announce.get_link())

# close the cursor object
cursor.close()

# close the connection
connection.close()
