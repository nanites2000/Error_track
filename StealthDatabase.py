import sqlite3
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import string



global finalFix
global initial
global startTime
global timerRunning
timerRunning =False
startTime = time.time()


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
def updateTimer():
    global startTime
    print("timer")
    timerString.set(str(round(time.time()-startTime)))
    root.after(1000,updateTimer)

def initialSelected(*args):
    global startTime
    global timerRunning
    print("Selected Initial")
    finalTime = time.time() - startTime
    print(finalTime)
    startTime = time.time()
    if not timerRunning:
        timerRunning = True
        updateTimer()

def setInitialListbox():
    global initial
    initial = getOptions("InitialProblem.txt")
    initialStrings = StringVar(value=initial)
    initialList["listvariable"] = initialStrings #this line actually changes the GUI

def setFinalFixListbox():
    global finalFix
    finalFix = getOptions("FinalFix.txt")
    finalFixStrings = StringVar(value=finalFix)
    finalFixList["listvariable"] = finalFixStrings

    #l.bind('<<ListboxSelect>>', profileSelected)

#this will actually submit the changes to  the sql database
def submit(*args):
    global initial
    global finalFix
    global startTime

    # sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    #    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
    # cursor.execute(sql_command)
    print(initialList.curselection()[0])
    initialValue= initial[initialList.curselection()[0]].strip()

    finalFixValue = finalFix[finalFixList.curselection()[0]].strip()

    if initial and finalFixValue:
        noteString= noteEntry.get()
        print(str(datetime.date)+ str(time.time()-startTime)+ str(initialValue)+str(finalFixValue)+str( noteString))
        sql_command = "INSERT INTO stealthErrors (date,StartTime, duration,InitialProblem,finalFix, note) VALUES (%s, %s, '%s', '%s', '%s');" % (
        datetime.today().strftime(), time.time()-startTime, initialValue,finalFixValue, noteString)
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







root = Tk()
root.title("Enter Errors")
root.geometry("1660x1000")

mainframe = ttk.Frame(root, padding="15 15 15 15")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

blenderInitial = StringVar()
meters = StringVar()
noteText = StringVar()

#initial frame
initialFrame = ttk.Frame(mainframe)
initialFrame.grid(column=0, row= 1)
initialLabel = ttk.Label(initialFrame, text="Initial Problem:")
initialLabel.grid(column=0, row=0)
initialLabel.config(font=("Courier", 30))

initialList=Listbox(initialFrame,height=21, width=45,exportselection=0)
initialList.grid(row=1, column=0,rowspan=14, sticky=(N,W,E))
scrollInitial = ttk.Scrollbar(initialFrame, orient=VERTICAL, command=initialList.yview)
scrollInitial.grid(column=1, row=0,sticky = (N,S,W), rowspan = 10)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
initialList.configure(yscrollcommand=scrollInitial.set)
initialList.config(font=("Courier", 20))
#root.columnconfigure(0,)



#finalFix Frame
finalFixFrame = ttk.Frame(mainframe)
finalFixFrame.grid(column=1, row= 1)
finalFixLabel = ttk.Label(finalFixFrame, text="Final Fix:")
finalFixLabel.grid(column=0, row=0)
finalFixLabel.config(font=("Courier", 30))

finalFixList=Listbox(finalFixFrame,height=15, width=20,exportselection=0)
finalFixList.grid(row=1, column=0,rowspan=14, sticky=(N,W,E))
s = ttk.Scrollbar( finalFixFrame, orient=VERTICAL, command=finalFixList.yview)
s.grid(column=1, row=0,sticky = (N,S,W), rowspan = 10)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
finalFixList.configure(yscrollcommand=s.set)
finalFixList.config(font=("Courier", 30))
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

#set up the button frame
buttonFrame = ttk.Frame(root)
buttonFrame.grid(column = 2, row=0, sticky =(W))


timerLabel = Label(buttonFrame, text="Timer:")
timerLabel.grid(row = 0, column = 0,sticky =(W))
timerLabel.config(font=("Courier", 45))


timerString = StringVar()
timer = Label(buttonFrame,textvariable = timerString)
timer.grid(row = 1, column = 0)
timer.config(font=("Courier bold", 75))
timerString.set("0")



submitButton = Button(buttonFrame, text="Submit", command=submit)
submitButton.grid(column=0, row=2, sticky=W)
submitButton.config(font=("Courier", 30))
submitButton.config(bg=("light blue"))




for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
setInitialListbox()
setFinalFixListbox()
#feet_entry.focus()
root.bind('<Return>', submit)
initialList.bind('<<ListboxSelect>>', initialSelected)


root.mainloop()


