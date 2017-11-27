import sqlite3
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import string





times = datetime.now().strftime("\'%T:%f\'")
dates= time.strftime("'%F'")


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




#this will actually submit the changes to  the sql database
def submit(*args):


    # sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    #    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
    # cursor.execute(sql_command)
    model= blenderModel.get()
    detail = '"asg"'''
    sql_command = "INSERT INTO stealthErrors (dates,times,blenderModel,errorCode,errorDetail,note) VALUES (%s, %s, '%s', 'ctap', '%s', 'the screw broke');" % (
    dates, times, model, detail)
    cursor.execute(sql_command)

    #cursor.execute("SELECT * FROM stealthErrors")
    #print("\nfetch one:")
    #res = cursor.fetchone()
   # print(res)

    cursor.execute("SELECT * FROM stealthErrors")
    print("fetchall:")
    result = cursor.fetchall()
    for r in result:
        print(r)



    # never forget this, if you want the changes to be saved:
    connection.commit()

    #





root = Tk()
root.title("Enter Errors")
root.geometry("1360x750")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

blenderModel = StringVar()
meters = StringVar()

modelFrame = ttk.Frame(mainframe)
modelFrame.grid(column=3, row= 1)
ttk.Label(modelFrame, text="Blender Model:").grid(column=0, row=1, sticky=W)
blenderModelEntry = ttk.Entry(modelFrame, width=7, textvariable=blenderModel)
blenderModelEntry.grid(column=1, row=1, sticky=(W))

noteFrame = ttk.Frame(mainframe)
noteFrame.grid(column=3, row= 2)
ttk.Label(modelFrame, text="Blender Model:").grid(column=0, row=1, sticky=W)
blenderModelEntry = ttk.Entry(modelFrame, width=7, textvariable=blenderModel)
blenderModelEntry.grid(column=1, row=1, sticky=(W))


ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Submit", command=submit).grid(column=3, row=3, sticky=W)


ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#feet_entry.focus()
root.bind('<Return>', submit)

root.mainloop()


