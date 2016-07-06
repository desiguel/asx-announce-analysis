#!/usr/bin/python3

from announcement import Announcement
from database import Database

# Connect to the database and return cursor
local_database = Database()
cursor = local_database.get_cursor()
cursor.execute("Select * from company_announcements where link ='01106368'")

# fetch a single row using fetchone() method.
row = cursor.fetchone()
for row in cursor:
    print(row)
    test_announce = Announcement(*row)
    print(test_announce.get_link())
    print(test_announce.get_pdf_link())
    raw_announce = test_announce.get_text()
    clean_text = test_announce.clean_text(raw_announce)
    print(test_announce.tokenised())

# close the cursor object
cursor.close()

# close the connection
local_database.close_connection()
