import tkinter as tk
from backend import backend
#from tkinter import messagebox

class projectInputNameBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Project:")
        self.geometry("500x250+500+300")

        self.getProjectInfo = backend()
        self.nextBoolean = 0

        self.projectID = ""

    def on_closing(self):
            self.boolToReturn = 0
            self.quit()
            self.destroy()

    def addNewProject(self):
        dateOne = self.stDate1.get() + "/" + self.stDate2.get() + "/" + self.stDate3.get()
        dateTwo = self.edDate1.get() + "/" + self.edDate2.get() + "/" + self.edDate3.get()

        if self.projectID != "" and self.projectNmae.get() != "" and self.projectDiscp.get() != "" and dateOne != "" and dateTwo != "":
            self.getProjectInfo.addProjectsToDatabase(self.projectID, self.projectNmae.get(), self.projectDiscp.get(), dateOne, dateTwo)
            self.nextBoolean = 1

    def updateProject(self):
        dateOne = self.stDate1.get() + "/" + self.stDate2.get() + "/" + self.stDate3.get()
        dateTwo = self.edDate1.get() + "/" + self.edDate2.get() + "/" + self.edDate3.get()

        if self.projectID != "" and self.projectNmae.get() != "" and self.projectDiscp.get() != "" and dateOne != "" and dateTwo != "":
            self.getProjectInfo.updateProjectTable(self.projectID, self.projectNmae.get(), self.projectDiscp.get(), dateOne, dateTwo)
            self.nextBoolean = 1

    def getProjectsDataUsingProjectID(self):
        dataList = self.getProjectInfo.getProjectIDForProjectInputPopup(self.projectID)

        if self.projectID == "":
            self.projectNmae.insert(-1, "")
            self.projectDiscp.insert(-1, "")

            self.stDate1.insert(-1, "")
            self.stDate2.insert(-1, "")
            self.stDate3.insert(-1, "")

            self.edDate1.insert(-1, "")
            self.edDate2.insert(-1, "")
            self.edDate3.insert(-1, "")

        else:
            self.projectNmae.insert(-1, dataList[1])
            self.projectDiscp.insert(-1, dataList[2])

            date01 = dataList[3].split("/")
            date02 = dataList[4].split("/")

            self.stDate1.insert(-1, date01[0])
            self.stDate2.insert(-1, date01[1])
            self.stDate3.insert(-1, date01[2])

            self.edDate1.insert(-1, date02[0])
            self.edDate2.insert(-1, date02[1])
            self.edDate3.insert(-1, date02[2])

        self.projectID = dataList[0]

    def popUpBoxInput(self):

        # Project Name Frame
        frame1 = tk.Frame(self)
        frame1.pack(fill="x")

        lbl1 = tk.Label(frame1, text="Project Name", width=10)
        lbl1.pack(side="left", padx=5, pady=10)

        self.projectNmae = tk.Entry(frame1)
        self.projectNmae.pack(fill="x", padx=5, pady=10)

        # Project discription Frame
        frame2 = tk.Frame(self)
        frame2.pack(fill="x")

        lbl2 = tk.Label(frame2, text="Description", width=10)
        lbl2.pack(side="left", padx=5, pady=10)

        self.projectDiscp = tk.Entry(frame2)
        self.projectDiscp.pack(fill="x", padx=5, expand=True)


        # Project date 01 Frame
        frame4 = tk.Frame(self)
        frame4.pack(fill="x")

        lbl4 = tk.Label(frame4, text="Start Date: ", width=10)
        lbl4.pack(side="left", padx=5, pady=10)

        self.stDate1 = tk.Entry(frame4, width=5)
        self.stDate1.pack(side="left", padx=5, pady=10) #


        lbl5 = tk.Label(frame4, text=" / ", width=2)
        lbl5.pack(side="left", padx=5, pady=10)

        self.stDate2 = tk.Entry(frame4, width=5)
        self.stDate2.pack(side="left", padx=5, pady=10) 

        lbl6 = tk.Label(frame4, text=" / ", width=2)
        lbl6.pack(side="left", padx=5, pady=10)

        self.stDate3 = tk.Entry(frame4, width=10)
        self.stDate3.pack(side="left", padx=5, pady=10) 


        # Project date 02 Frame
        frame5 = tk.Frame(self)
        frame5.pack(fill="x")

        lbl7 = tk.Label(frame5, text="Ending Date: ", width=10)
        lbl7.pack(side="left", padx=5, pady=10)

        self.edDate1 = tk.Entry(frame5, width=5)
        self.edDate1.pack(side="left", padx=5, pady=10) #


        lbl8 = tk.Label(frame5, text=" / ", width=2)
        lbl8.pack(side="left", padx=5, pady=10)

        self.edDate2 = tk.Entry(frame5, width=5)
        self.edDate2.pack(side="left", padx=5, pady=10) 


        lbl9 = tk.Label(frame5, text=" / ", width=2)
        lbl9.pack(side="left", padx=5, pady=10)

        self.edDate3 = tk.Entry(frame5, width=10)
        self.edDate3.pack(side="left", padx=5, pady=10) 

        # Project submit
        frame3 = tk.Frame(self)
        frame3.pack(fill="x")

        self.submitButton = tk.Button(frame3, text="Submit")
        self.submitButton.pack(padx=5, pady=10)

        