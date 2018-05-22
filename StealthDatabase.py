import sqlite3
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import string


global errors
global models



#times = datetime.now().strftime("\'%T:%f\'")
#dates= time.strftime("'%F'")


connection = sqlite3.connect("company.db")

cursor = connection.cursor()

# delete
#cursor.execute("""DROP TABLE stealthErrors;""")



#this creates the table if it doesn't already exist.
sql_command = """
CREATE TABLE  IF NOT EXISTS stealthErrors ( 
RowID INTEGER PRIMARY KEY , 
Date DATE,
StartTime TIME,
EndTime TIME,
Duration REAL,
InitialProblem TEXT,
FinalFix TEXT, 
Note TEXT
);"""
cursor.execute(sql_command)

def getOptions(file):
    filename = "configuration\\" + file
    print(filename)
    with open (filename) as f:
        result = f.readlines()

    return(result)




def setModelListbox():
    global models
    models = getOptions("InitialProblem.txt")
    modelStrings = StringVar(value=models)
    modelList["listvariable"] = modelStrings #this line actually changes the GUI

def setErrorListbox():
    global errors
    errors = getOptions("FinalFix.txt")
    errorStrings = StringVar(value=errors)
    errorList["listvariable"] = errorStrings

    #l.bind('<<ListboxSelect>>', profileSelected)

#this will actually submit the changes to  the sql database
def submit(*args):


    # sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    #    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
    # cursor.execute(sql_command)
    model= models[modelList.curselection()[0]].strip()
    detail = ''
    errorCode = errors[errorList.curselection()[0]].strip()
    noteString= noteEntry.get()
    sql_command = "INSERT INTO stealthErrors (dates,times,blenderModel,errorCode,errorDetail,note) VALUES (%s, %s, '%s', '%s', '%s', '%s');" % (
    dates, times, model,errorCode, detail,noteString)
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
noteText = StringVar()

#model frame
modelFrame = ttk.Frame(mainframe)
modelFrame.grid(column=0, row= 1)
modelLabel = ttk.Label(modelFrame, text="Initial Problem:")
modelLabel.grid(column=0, row=0)
modelLabel.config(font=("Courier", 30))

modelList=Listbox(modelFrame,height=21, width=45,exportselection=0)
modelList.grid(row=1, column=0,rowspan=14, sticky=(N,W,E))
scrollModel = ttk.Scrollbar(modelFrame, orient=VERTICAL, command=modelList.yview)
scrollModel.grid(column=1, row=0,sticky = (N,S,W), rowspan = 10)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
modelList.configure(yscrollcommand=scrollModel.set)
modelList.config(font=("Courier", 20))
#root.columnconfigure(0,)



#error Frame
errorFrame = ttk.Frame(mainframe)
errorFrame.grid(column=1, row= 1)
errorLabel = ttk.Label(errorFrame, text="Final Fix:")
errorLabel.grid(column=0, row=0)
errorLabel.config(font=("Courier", 30))

errorList=Listbox(errorFrame,height=15, width=20,exportselection=0)
errorList.grid(row=1, column=0,rowspan=14, sticky=(N,W,E))
s = ttk.Scrollbar( errorFrame, orient=VERTICAL, command=errorList.yview)
s.grid(column=1, row=0,sticky = (N,S,W), rowspan = 10)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
errorList.configure(yscrollcommand=s.set)
errorList.config(font=("Courier", 30))
#root.columnconfigure(0,)





#note frame
noteFrame = ttk.Frame(root)
noteFrame.grid(column=0, row= 1, columnspan = 30)
noteLabel = ttk.Label(noteFrame, text="Note:")
noteLabel.grid(column=0, row=0,sticky =E)
noteLabel.config(font=("Courier", 22))
noteEntry = ttk.Entry(noteFrame, width=250, textvariable=noteText)
noteEntry.grid(column=1, columnspan = 30, row = 0)
noteEntry.config(font=("Courier", 22))






submitButton = Button(root, text="Submit", command=submit)
submitButton.grid(column=1, row=5, sticky=W)
submitButton.config(font=("Courier", 30))
submitButton.config(bg=("light blue"))




for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
setModelListbox()
setErrorListbox()
#feet_entry.focus()
root.bind('<Return>', submit)

root.mainloop()


