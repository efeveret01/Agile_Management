import tkinter as tk
from tkinter import ttk

from click import command
from backend import backend

class inputSprintItemPopup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Project:")
        self.geometry("600x400+500+300") #Width Hight x-position y-position

        self.getProjectInfo = backend()
        
        self.hidOption = 0
        self.sprintItemID = ""
        self.projectID = ""
        self.sprintID = ""
        self.boolToReturn = 0
    
    def closeWindow(self):
        self.quit()
        self.destroy()

    def updateTable(self, event):
        self.resetTable()

    def OnDoubleClick(self, event):
        print(self.table.item(self.table.focus())['text'])
        print(self.table.item(self.table.focus())['values'])
        print(self.table.item(self.table.focus())['values'][0])
        self.sprintItemID = self.table.item(self.table.focus())['text']
        self.secondStageOfPopup()


    def resetThelowerWindow(self):
        for widget in self.hiddenFrame.winfo_children():
                    widget.destroy()

    def cancelOption(self):
        self.resetThelowerWindow()
        #self.table.bind("<Double-1>", self.OnDoubleClick)
        self.hidOption = 0
        self.sprintItemID = ""
        self.populateHiddenArea()

    def secondStageOfPopup(self):
        self.resetThelowerWindow()
        self.hidOption = 1
        self.populateHiddenArea()

    def deleteTheProjectToDatabase(self):
        self.getProjectInfo.deleteSpecificSprintItem(self.sprintItemID)
        self.resetTable()    
        self.cancelOption()

    def addTheProjectToDatabase(self):
        if self.sprintItemEntry.get() != "":
            holdVar01 = self.projCombox.get()
            holdVar01 = holdVar01.split(")")

            self.getProjectInfo.addOrUpdateTheSprintItem(self.sprintItemID, self.sprintItemEntry.get(), self.itemStatues.get(), self.sprintID, holdVar01[0])
            self.resetTable()
            
            self.cancelOption()

    def populateProjectComboBax(self):
        choices = []
        for numofRows in range(len(self.getProjectInfo.populateProductBacklogTablePage(self.projectID))):
            projectItem = self.getProjectInfo.populateProductBacklogTablePage(self.projectID)[numofRows][2]
            tempHold = projectItem.split(", SEPERATION01A ")
            look = "As a user, " + tempHold[0] + ", so I can " + tempHold[1]

            contentO1 = self.getProjectInfo.populateProductBacklogTablePage(self.projectID)[numofRows][0] + ") " + look
            choices.append(contentO1)

        self.projCombox['values'] = choices
        if len(choices) != 0:
            self.projCombox.set(choices[0])

    def resetTable(self):

        self.table.delete(*self.table.get_children())

        holdVar01 = self.projCombox.get()
        holdVar01 = holdVar01.split(")")

        for  numofRows in range(len(self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID))):  # COMPLETED
            xxx = self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID)[numofRows][1]
            self.table.insert(parent='',index='end', text=self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID)[numofRows][0], values=(xxx, ))

    def resetTableWithEvent(self, event):

        self.table.delete(*self.table.get_children())

        holdVar01 = self.projCombox.get()
        holdVar01 = holdVar01.split(")")

        for  numofRows in range(len(self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID))):  # COMPLETED
            xxx = self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID)[numofRows][1]

            self.table.insert(parent='',index='end', text=self.getProjectInfo.populateTheSprintItemInputSecondTable(holdVar01[0],self.sprintID)[numofRows][0], values=(xxx, ))

    def populateHiddenArea(self):
        frame3 = tk.Frame(self.hiddenFrame, height=20)
        frame3.pack(anchor="c",fill="x")
        
        btn = tk.Button(frame3, text="Add Item", command=self.secondStageOfPopup)

        if self.hidOption == 0:
            btn.pack(side= "left", padx=5, pady=10)
            self.geometry("600x400")
            self.table.bind("<Double-1>", self.OnDoubleClick)
        else:
            self.table.unbind("<Double-1>")

            self.geometry("600x450")
            hiddenFrame01 = tk.Frame(self.hiddenFrame)
            hiddenFrame01.pack(fill="x")

            lbl1 = tk.Label(hiddenFrame01, text="Input Sprint Item: ", width=15)
            lbl1.configure(anchor="w")
            lbl1.pack(fill= "x", padx=5, pady=2)

            self.sprintItemEntry = tk.Entry(hiddenFrame01)
            self.sprintItemEntry.pack(padx=10, fill="x")

            hiddenFrame02 = tk.Frame(self.hiddenFrame)
            hiddenFrame02.pack(fill="x")

            choices = ["Not Started", "W.I.P", "Completed"]
            variable = tk.StringVar()
            self.itemStatues = ttk.Combobox(hiddenFrame02, textvariable=variable, width=10)
            self.itemStatues['values'] = choices
            self.itemStatues['state'] = 'readonly' 
            self.itemStatues.set("Not Started")
            self.itemStatues.pack(side="left", padx=10, pady=15) #

            addOrUpdateButton =  tk.Button(hiddenFrame02, text="Add/Update Selected", command=self.addTheProjectToDatabase)
            addOrUpdateButton.pack(side="right", fill="x", padx=10)

            deleteButton =  tk.Button(hiddenFrame02, text="Delete", command=self.deleteTheProjectToDatabase)
            deleteButton.pack(side="right", fill="x", padx=10)

            cancelButton =  tk.Button(hiddenFrame02, text="Cancel", command=self.cancelOption)
            cancelButton.pack(side="right", fill="x", padx=10)

            self.sprintItemEntry.insert(0, self.getProjectInfo.getTheSprintItemRecords(self.sprintItemID)[0])
            self.itemStatues.set(self.getProjectInfo.getTheSprintItemRecords(self.sprintItemID)[1])
            #self.getProjectInfo.getTheSprintItemRecords(self.sprintItemID)    e.insert(0,text)

    def popUpBoxInput(self):
        # Project Name Frame
        frame1 = tk.Frame(self)
        frame1.pack(fill="x")

        lbl1 = tk.Label(frame1, text="Select Product Backlog: ", width=15)
        lbl1.configure(anchor="w")
        lbl1.pack(fill= "x", padx=5, pady=2)


        variable = tk.StringVar()
        self.projCombox = ttk.Combobox(frame1, textvariable=variable, width=30)
        self.projCombox['state'] = 'readonly'  
        self.projCombox.pack(fill="x", padx=5, pady=2) #
        self.projCombox.bind("<<ComboboxSelected>>", self.resetTableWithEvent)


        # Project discription Frame
        frame2 = tk.Frame(self)
        frame2.pack(fill="x")

        lbl2 = tk.Label(frame2, text="Product Sprint Items:", width=10)
        lbl2.configure(anchor="w")
        lbl2.pack(fill="x", padx=5, pady=10)

        # Table
        self.table = ttk.Treeview(frame2)
        self.table['columns'] = ('sprint_log')
        self.table.column("#0", width=0,  stretch="no")
        self.table.column("sprint_log",anchor="center",width=200)
        self.table.heading("#0",text="",anchor="center")
        self.table.heading("sprint_log",text="SPRINT ITEMS",anchor="center")
        self.table.pack(fill="x", padx=4)
        

        # Project submit
        self.hiddenFrame = tk.Frame(self)
        self.hiddenFrame.pack(fill="x")
        
        self.populateProjectComboBax()
        self.resetTable()
        self.populateHiddenArea()
