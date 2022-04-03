import tkinter as tk
from tkinter import ttk
from backend import backend

class projBacklogInputBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Product Backlog Items:")
        self.geometry("500x200+500+300")

        self.getProjectInfo = backend()

        self.projectItemID = ""
        self.projectID = ""
        self.nextBoolean = 0
        self.addOrUpdate = 0



    def closeWindow(self):
        self.quit()
        self.destroy()

    def deleteTheProductItemsToDatabase(self):
        self.getProjectInfo.deleteSpecificProjectBacklog(self.projectItemID)

    def addTheProductItemsToDatabase(self):
        mergeDis = self.entry1.get() + ", SEPERATION01A " + self.entry2.get()

        if self.entry1.get() != "" and self.entry2.get() != "" and self.priority.get() != "" and self.statues.get() != "":
            self.nextBoolean = 1
            self.getProjectInfo.updateProductLogItemTable(self.projectItemID, self.priority.get(), mergeDis, self.statues.get(), self.projectID, self.addOrUpdate)

    def popUpBoxInput(self, projectItemID, projectID):
        boxDATA =  self.getProjectInfo.getNewProjectBacklogItemsIDs(projectItemID, projectID)

        gotSections = ""

        if projectItemID != "":
            self.addOrUpdate = 1
            gotSections = boxDATA[2]
            gotSections = gotSections.split(", SEPERATION01A ")
        else:
            self.addOrUpdate = 0
            gotSections = ["",""]

        self.projectItemID = boxDATA[0]
        self.projectID = projectID

        # Project Name Frame
        frame1 = tk.Frame(self)
        frame1.pack(fill="x")

        
        lbl1 = tk.Label(frame1, text="As a user: ", width=10)
        lbl1.pack(side="left", padx=5, pady=10)

        name = tk.StringVar(frame1, value=gotSections[0])
        self.entry1 = tk.Entry(frame1, textvariable=name)
        self.entry1.pack(fill="x", padx=5, pady=10) # 

        # Project discription Frame
        frame2 = tk.Frame(self)
        frame2.pack(fill="x")

        lbl2 = tk.Label(frame2, text="So I can: ", width=10)
        lbl2.pack(side="left", padx=5, pady=10)

        name = tk.StringVar(frame1, value=gotSections[1])
        self.entry2 = tk.Entry(frame2, textvariable=name)
        self.entry2.pack(fill="x", padx=5, expand=True)

        # Project date 01 Frame
        frame4 = tk.Frame(self)
        frame4.pack(fill="x")

        lbl4 = tk.Label(frame4, text="Priority: ", width=10)
        lbl4.pack(side="left", padx=5, pady=10)

        name = tk.StringVar(frame4, value=boxDATA[1])
        self.priority = tk.Entry(frame4, textvariable=name, width=8)
        #self.priority.insert("END", 'You email here')
        self.priority.pack(side="left", padx=5, pady=10) #

        lbl5 = tk.Label(frame4, text="Statues: ", width=10)
        lbl5.pack(side="left", padx=5, pady=10)


        choices = ['Not Started', 'In Progress', 'Complete']
        variable = tk.StringVar()
        
        self.statues = ttk.Combobox(frame4, textvariable=variable, width=15)

        if projectItemID == "":
            self.statues.set('Not Started')
        else:
            self.statues.set(boxDATA[3])

        #self.statues.set('Not Started')
        # prevent typing a value
        self.statues['values'] = choices
        self.statues['state'] = 'readonly'  
        self.statues.pack(side="left", padx=5, pady=10) #

        # Project submit
        frame3 = tk.Frame(self, padx=150)
        frame3.pack(anchor="c",fill="x")

        # # Command tells the form what to do when the button is clicked
        self.submitButton = tk.Button(frame3, text="Submit")
        self.submitButton.pack(side= "left", padx=5, pady=10)


        self.deleteButton = tk.Button(frame3, text="Delete")
        #self.deleteButton.configure(command=self.deleteTheProductItemsToDatabase)
        self.deleteButton.pack(side= "right", padx=5, pady=10)

        
