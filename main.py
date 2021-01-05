from activity import Activity
import datetime
import sqlite3
import time

db = sqlite3.connect("database.db")
cursor = db.cursor()

#sleep1 = Activity("Konstantin", "sleep", "03/01/2021 22:00")
# my_date = datetime.datetime.now()
# cursor.execute("INSERT INTO ACTIVITIES (USER_ID, START_DATE, ACTIVITY_TYPE) VALUES (?, ?, ?)", (1, my_date, 2))
# cursor.execute("UPDATE ACTIVITIES SET END_DATE = ? WHERE ID = ?", (datetime.datetime.now(), cursor.lastrowid))
# db.commit()
#
# cursor.execute("SELECT * from ACTIVITIES")
# #cursor.execute("SELECT last_insert_rowid()")
# print(cursor.lastrowid)
# print(cursor.fetchall())

# user = 1, activity = 3
a = Activity(1, 3)
a.start_activity(cursor)
db.commit()
time.sleep(20)
a.end_activity(cursor)
db.commit()

