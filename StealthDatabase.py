import sqlite3
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import string


global errors



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

def getOptions(file):
    filename = "configuration\\" + file
    print(filename)
    with open (filename) as f:
        result = f.readlines()

    return(result)

def setErrorListbox():
    global errors
    errors = getOptions("errors.txt")
    errorStrings = StringVar(value=errors)
    errorList["listvariable"] = errorStrings

    #l.bind('<<ListboxSelect>>', profileSelected)




#this will actually submit the changes to  the sql database
def submit(*args):


    # sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    #    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
    # cursor.execute(sql_command)
    model= blenderModel.get()
    detail = '"asg"'''
    errorCode = errors[errorList.curselection()[0]].strip()
    sql_command = "INSERT INTO stealthErrors (dates,times,blenderModel,errorCode,errorDetail,note) VALUES (%s, %s, '%s', '%s', '%s', 'the screw broke');" % (
    dates, times, model,errorCode, detail)
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
root.geometry("1660x1000")

mainframe = ttk.Frame(root, padding="15 15 15 15")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

blenderModel = StringVar()
meters = StringVar()

#model frame
modelFrame = ttk.Frame(mainframe)
modelFrame.grid(column=0, row= 1)
ttk.Label(modelFrame, text="Blender Model:").grid(column=0, row=1)
blenderModelEntry = ttk.Entry(modelFrame, width=7, textvariable=blenderModel)
blenderModelEntry.grid(column=1, row=1, sticky=(E))


#error Frame
errorFrame = ttk.Frame(mainframe)
errorFrame.grid(column=1, row= 1)
errorLabel = ttk.Label(errorFrame, text="Error:")
errorLabel.grid(column=0, row=0)
errorLabel.config(font=("Courier", 30))



errorList=Listbox(errorFrame,height=15, width=30)
errorList.grid(row=1, column=0,rowspan=14, sticky=(N,W,E))
s = ttk.Scrollbar( root, orient=VERTICAL, command=errorList.yview)
s.grid(column=1, row=0,sticky = (N,S,W), rowspan = 10)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
errorList.configure(yscrollcommand=s.set)
errorList.config(font=("Courier", 30))
#root.columnconfigure(0,)





#note frame
noteFrame = ttk.Frame(root)
noteFrame.grid(column=0, row= 1, columnspan = 30)
ttk.Label(noteFrame, text="Note:").grid(column=0, row=0,sticky =E)
noteEntry = ttk.Entry(noteFrame, width=250, textvariable=blenderModel)
noteEntry.grid(column=1, columnspan = 30, row = 0)







submitButton = Button(root, text="Submit", command=submit)
submitButton.grid(column=1, row=5, sticky=W)
submitButton.config(font=("Courier", 30))
submitButton.config(bg=("light blue"))




for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

setErrorListbox()
#feet_entry.focus()
root.bind('<Return>', submit)

root.mainloop()


