import pyodbc
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import string
import pyautogui
import time
import numpy as np

global finalFix
global initial
global startTime
global timerRunning
timerRunning = False
startTime = time.time()

connection = pyodbc.connect("DRIVER={SQL Server}; server=DAXSQL01; uid = EngSQLSvc; pwd = cpUAk(20uTzW)")


cursor = connection.cursor()

# delete
# cursor.execute("""DROP TABLE stealthErrors;""")


'''
# this creates the table if it doesn't already exist.
sql_command = """
CREATE TABLE  IF NOT EXISTS stealthErrors ( 
RowID INTEGER PRIMARY KEY , 
datetime TEXT,
Duration REAL,
InitialProblem TEXT,
FinalFix TEXT, 
Note TEXT
);"""
cursor.execute(sql_command)
'''

class MyDialog:
    def __init__(self, parent):

        top = self.top = Toplevel(parent)
        self.TopLabel = Label(top, text='Enter the information below:')
        self.TopLabel.grid(row=0, column=1)
        self.TopLabel.config(font=("Courier", 15))

        self.mySubmitButton = Button(top, text='Submit', command=self.send)
        self.mySubmitButton.grid(row=4, column=1)
        self.mySubmitButton.config(font=("Courier", 35))
        self.mySubmitButton.config(bg=("light blue"))

        self.myQuitButton = Button(top, text='Quit', command=self.quitter)
        self.myQuitButton.grid(row=4, column=2)
        self.myQuitButton.config(font=("Courier", 35))
        self.myQuitButton.config(bg=("red"))

        self.operatorLabel = Label(top, text='Select Shift')
        self.operatorLabel.grid(row=1, column=0)
        self.operatorLabel.config(font=("Courier", 15))

        # with open('operators.txt') as f:
        #   operators = f.read().splitlines()
        self.operatorName = StringVar(value=["First", "Second", "Third", "All Shifts"])
        self.operatorListbox = Listbox(top, height=4, listvariable=self.operatorName, exportselection=0)
        self.operatorListbox.grid(row=2, column=0)
        self.operatorListbox.config(font=("Courier", 15))
        self.operatorListbox.selection_set(0)

        self.machineLabel = Label(top, text='Select Timeframe')
        self.machineLabel.grid(row=1, column=1)
        self.machineLabel.config(font=("Courier", 15))

        # with open('machines.txt') as f:
        #   machines = f.read().splitlines()
        self.machines = StringVar(value=["Today", "Month", "Previous Month"])
        self.machineListbox = Listbox(top, height=4, listvariable=self.machines, exportselection=0)
        self.machineListbox.grid(row=2, column=1)
        self.machineListbox.config(font=("Courier", 15))
        self.machineListbox.selection_set(0)

        self.orderLabel = Label(top, text='Select Sort Order')
        self.orderLabel.grid(row=1, column=2)
        self.orderLabel.config(font=("Courier", 15))

        self.order = StringVar(value=["Count", "Total Time"])
        self.orderListbox = Listbox(top, height=2, listvariable=self.order, exportselection=0)
        self.orderListbox.grid(row=2, column=2, sticky=(N))
        self.orderListbox.config(font=("Courier", 15))
        self.orderListbox.selection_set(0)

        self.textbox = Text(top, height=25, width=90)
        self.textbox.grid(row=5, column=0, columnspan=3)
        self.textbox.config(font=("Courier", 15))


        # self.operatorListbox.bind('<<ListboxSelect>>', listboxSelected)
        # self.machineListbox.bind('<<ListboxSelect>>', listboxSelected)

    def send(self):

        # self.userSelected = self.operatorListbox.get(self.operatorListbox.curselection())
        # self.machineSelected = self.machineListbox.get(self.machineListbox.curselection())
        # self.partSelected = self.partListbox.get(self.partListbox.curselection())
        # shift = self.operatorListbox.get(self.operatorListbox.curselection())
        # timeframe= self.machineListbox.get(self.machineListbox.curselection())
        shift = self.operatorListbox.get(self.operatorListbox.curselection())
        timeframe = self.machineListbox.get(self.machineListbox.curselection())
        sortby = self.orderListbox.get(self.orderListbox.curselection())

        # code to actually send sql query

        timecode = ""
        if timeframe == "Today":
            timecode = "CONVERT(date, datetime) = CONVERT(date, GETDATE())"
        elif timeframe == "Month":
            timecode = "DATENAME(mm,datetime) = DATENAME(mm,GETDATE())"
        elif timeframe == "Previous Month":
           timecode=" datetime >= dateadd(month, datediff(month, 1, GETDATE()), 0) AND datetime < dateadd(month, datediff(month, 0, GETDATE()), 0)"
           # timecode = "strftime('%m',date(datetime)) =  strftime('%m','now', '-1 month')"

        if shift == "First":
            shiftcode = "CONVERT(time,datetime) BETWEEN '06:00:00' and '14:15:00 '"
        elif shift == "Second":
            shiftcode = "CONVERT(time,datetime) BETWEEN '14:15:00' and '22:15:00'"
        else:
            shiftcode = "6=6"

        sortcode = ""
        if sortby == "Count":
            sortcode = "countProblems"
        elif sortby == "Total Time":
            sortcode = "sumDuration"

        self.textbox.delete(1.0, END)
        # statement = "select InitialProblem, count(InitialProblem), sum(Duration) from stealthErrors GROUP BY InitialProblem HAVING ?"
        statement = "select InitialProblem, count(InitialProblem) as countProblems, sum(Duration) as sumDuration from [PRODUCTION_REC].[dbo].[testing4StealthErrors] WHERE %s AND %s GROUP BY InitialProblem ORDER BY %s desc" % (

        #statement = "select InitialProblem, count(InitialProblem) as countProblems, sum(Duration) as sumDuration from stealthErrors WHERE %s AND %s GROUP BY InitialProblem ORDER BY %s desc" % (
        timecode, shiftcode, sortcode)
        cursor.execute(statement)

        result = cursor.fetchall()
        self.textbox.insert(END, 'Failure Name                              Count      Time (minutes)\n')
        totalCount = 0
        totalDuration = 0
        if result:
            for r in result:
                padding = 40 - len(r[0])
                countString = ('%5s' % r[1])
                durationString = '%6s' % round(r[2] / 60, 1)
                insertString = r[0] + '-' * padding + '>' + countString + ' ---->' + durationString + '\n'
                totalCount += r[1]
                totalDuration += r[2]
                self.textbox.insert(END, insertString)

        else:
            self.textbox.insert(END, "No Data Found\n")

        totalCountString = '%5s' % totalCount
        totalDurationString = '%6s' % round(totalDuration / 60, 1)
        insertString = "TOTALS" + '-' * 34 + '>' + totalCountString + ' ---->' + totalDurationString + '\n'
        self.textbox.insert(END, insertString)
        try:
            with open("/media/pi/DATA/data.txt", 'w') as F:
                textToWrite = self.textbox.get("1.0", END)
                F.write(textToWrite)
        except:
            print("usb write failure")

    def quitter(self):
        self.top.destroy()


def onClick():
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)


def keepAlive():
    # pyautogui.press('f15')
    # root.after(120000, keepAlive)
    pass


# sets up the items in the listboxes
def getOptions(file):
    filename = "configuration/" + file
    print(filename)
    with open(filename) as f:
        result = f.readlines()
        for index, line in enumerate(result):
            result[index] = line.strip()
    return (result)


# this function keeps the timer on the screen up to date and calls itsself every second to update
def updateTimer():
    global startTime
    timerString.set(str(round(time.time() - startTime)))
    if timerRunning == True:
        root.after(1000, updateTimer)
    else:
        timerString.set("0")


# this is what happens after the first listbox item is selected
def initialSelected(*args):
    global startTime
    global longStartTime
    global timerRunning
    startTime = time.time()
    now = datetime.now()
    longStartTime = nowTime = now.hour + now.minute / 60 + now.second / 3600
    if not timerRunning:
        timerRunning = True
        updateTimer()

    finalFixList.config(state=NORMAL)
    finalFixList.selection_clear(0, END)
    submitButton.config(bg=("light blue"))


def finalFixSelected(*args):
    try:
        initialValue = initial[initialList.curselection()[0]].strip()
    except:
        initialValue = False
    if initialValue:
        submitButton.config(bg=("green"))


# actually populates first listbox
def setInitialListbox():
    global initial
    initial = getOptions("InitialProblem.txt")
    initialStrings = StringVar(value=initial)
    initialList["listvariable"] = initialStrings  # this line actually changes the GUI


# actually populates second listbox
def setFinalFixListbox():
    global finalFix
    finalFix = getOptions("FinalFix.txt")
    finalFixStrings = StringVar(value=finalFix)
    finalFixList["listvariable"] = finalFixStrings

    # l.bind('<<ListboxSelect>>', profileSelected)


# this will actually submit the changes to  the sql database
def submit(*args):
    global initial
    global finalFix
    global startTime
    global longStartTime
    global timerRunning

    # sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    #    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
    # cursor.execute(sql_command)

    try:
        initialValue = initial[initialList.curselection()[0]].strip()
    except:
        initialValue = False
    try:
        finalFixValue = finalFix[finalFixList.curselection()[0]].strip()
    except:
        finalFixValue = False

    if initial and finalFixValue:
        noteString = noteEntry.get()
        now = datetime.now()
        timestring = now.strftime('%Y-%m-%d %X.%f')
        sql_command = "INSERT INTO [PRODUCTION_REC].[dbo].[testing4StealthErrors] (datetime, duration,InitialProblem,finalFix, note) VALUES (?, ?, ?, ?,?);"

        cursor.execute(sql_command, (timestring, time.time() - startTime, initialValue, finalFixValue, noteString))

        # cursor.execute("SELECT * FROM stealthErrors")
        # print("\nfetch one:")
        # res = cursor.fetchone()
        # print(res)


        # never forget this, if you want the changes to be saved:
        connection.commit()

        # reset everything back to default in the GUI

        initialList.selection_clear(0, END)
        finalFixList.selection_clear(0, END)
        finalFixList.config(state=DISABLED)
        noteEntry.delete(0, END)
        submitButton.config(bg=("light blue"))
        timerRunning = 0  # to stop the timer



    else:
        submitButton.config(bg=("red"))


def shiftReportButtonPressed():
    onClick()


root = Tk()
root.title("Enter Errors")
root.geometry("1660x1000")

mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

blenderInitial = StringVar()
meters = StringVar()
noteText = StringVar()

# initial frame
initialFrame = ttk.Frame(mainframe)
initialFrame.grid(column=0, row=1)
initialLabel = ttk.Label(initialFrame, text="1.Initial Problem:")
initialLabel.grid(column=0, row=0)
initialLabel.config(font=("Courier", 30))

initialList = Listbox(initialFrame, height=21, width=45, exportselection=0)
initialList.grid(row=1, column=0, rowspan=14, sticky=(N, W, E), padx="0")
scrollInitial = ttk.Scrollbar(initialFrame, orient=VERTICAL, command=initialList.yview)
scrollInitial.grid(column=1, row=0, sticky=(N, S, W), rowspan=10)
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)
initialList.configure(yscrollcommand=scrollInitial.set)
initialList.config(font=("Courier", 20))
# root.columnconfigure(0,)



# finalFix Frame
finalFixFrame = ttk.Frame(mainframe)
finalFixFrame.grid(column=1, row=1)
finalFixLabel = ttk.Label(finalFixFrame, text="2.Final Fix:")
finalFixLabel.grid(column=0, row=0)
finalFixLabel.config(font=("Courier", 30))

finalFixList = Listbox(finalFixFrame, height=15, width=20, exportselection=0)
finalFixList.grid(row=1, column=0, rowspan=14, sticky=(N, W))
s = ttk.Scrollbar(finalFixFrame, orient=VERTICAL, command=finalFixList.yview)
s.grid(column=1, row=0, sticky=(N, S, W), rowspan=10)
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)
finalFixList.configure(yscrollcommand=s.set)
finalFixList.config(font=("Courier", 30))
finalFixList.config(state=DISABLED)
# root.columnconfigure(0,)





# note frame
noteFrame = ttk.Frame(root)
noteFrame.grid(column=0, row=1, columnspan=30)

noteLabel = ttk.Label(noteFrame, text="Note:")
noteLabel.grid(column=0, row=0, sticky=E)
noteLabel.config(font=("Courier", 22))
noteEntry = ttk.Entry(noteFrame, width=250, textvariable=noteText)
noteEntry.grid(column=1, columnspan=30, row=0)
noteEntry.config(font=("Courier", 22))

# report buttons
reportFrame = ttk.Frame(root)
reportFrame.grid(column=0, row=2)

shiftReportButton = Button(reportFrame, text="Report", command=shiftReportButtonPressed)
shiftReportButton.grid(column=0, row=1)
shiftReportButton.config(font=("Courier", 30))
shiftReportButton.config(bg=("light blue"))

# set up the button frame
buttonFrame = ttk.Frame(root)
buttonFrame.grid(column=2, row=0, sticky=(W))

timerLabel = Label(buttonFrame, text="Timer:")
timerLabel.grid(row=0, column=0, sticky=(W))
timerLabel.config(font=("Courier", 45))

timerString = StringVar()
timer = Label(buttonFrame, textvariable=timerString)
timer.grid(row=1, column=0)
timer.config(font=("Courier bold", 75))
timerString.set("0")

submitButton = Button(buttonFrame, text="3.Submit", command=submit)
submitButton.grid(column=0, row=2, sticky=W)
submitButton.config(font=("Courier", 30))
submitButton.config(bg=("light blue"))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
setInitialListbox()
setFinalFixListbox()
# feet_entry.focus()
root.bind('<Return>', submit)
initialList.bind('<<ListboxSelect>>', initialSelected)
finalFixList.bind('<<ListboxSelect>>', finalFixSelected)
keepAlive()

root.mainloop()


