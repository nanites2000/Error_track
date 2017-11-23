import sqlite3
import time
from datetime import datetime

times = datetime.now().strftime("\'%T:%f\'")
dates= time.strftime("'%F'")
print("date:%s"%(dates))
print(times)

connection = sqlite3.connect("company.db")

cursor = connection.cursor()

# delete
#cursor.execute("""DROP TABLE stealthErrors;""")


#this creates the table if it doesn't already exist.
sql_command = """
CREATE TABLE  IF NOT EXISTS stealthErrors ( 
errorID INTEGER PRIMARY KEY , 
dates DATE,
times TIME,
blenderModel VARCHAR(50), 
errorCode VARCHAR(100) , 
errorDetail VARCHAR(300),
note VARCHAR(600)
);"""

cursor.execute(sql_command)

#sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
#cursor.execute(sql_command)


sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
cursor.execute(sql_command)
detail = '"asgsgsgs"sdfsdfgsdg"sdgsdgsdg"'''
sql_command = "INSERT INTO stealthErrors (dates,times,blenderModel,errorCode,errorDetail,note) VALUES (%s, %s, '5578', 'ctap', '%s', 'the screw broke');"%(dates,times, detail)
cursor.execute(sql_command)



cursor.execute("SELECT * FROM stealthErrors")
print("\nfetch one:")
res = cursor.fetchone()
print(res)

cursor.execute("SELECT * FROM stealthErrors")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

cursor.execute("SELECT * FROM stealthErrors WHERE blenderModel = 5578")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

# never forget this, if you want the changes to be saved:
connection.commit()

connection.close()