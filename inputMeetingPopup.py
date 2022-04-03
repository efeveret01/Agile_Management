import tkinter as tk
from tkinter import ttk
from backend import backend

class inputMeetingPopup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Product Backlog Items:")
        self.geometry("500x200+500+300")
        
        self.getProjectInfo = backend()
        
        self.frameOptions = "DMLogs"
        self.addOrUpdate = 0
        self.meeetingID = ""
        self.sprintID = ""
        self.tempHoldingID = ""
        self.MeetingSPTyeHolder = ""
        self.nextBoolean = 0
    
    def closeWindow(self):
        self.quit()
        self.destroy()

    def deleteMeetingLog(self):
        self.getProjectInfo.deleteSpecificMeetingLog(self.tempHoldingID, self.meetingType.get())

    def clearBotFrame(self):
        self.closeWindow()

    def clearMidSection(self, event):

        for widget in self.frameMid01.winfo_children():
            widget.destroy()

        self.optionalFrames(self.meetingType.get())

    def pushDataintoDatabase(self):

        mergeDates = self.meetingDate01.get()+ "/" + self.meetingDate02.get() + "/" + self.meetingDate03.get()

        if self.meetingType.get() == "Daily Meeting":
            mergeDis = self.dmFirstDisc.get() + ", SEPERATION01A " + self.dmSecondDisc.get() + ", SEPERATION01A " + self.dmThirdDisc.get()

            if self.meetingDate01.get() != "" and self.meetingDate02.get() != "" and self.meetingDate03.get() != "" and self.user.get() != "" and self.dmFirstDisc.get() != "" and self.dmSecondDisc.get() != "" and self.dmThirdDisc.get() != "":
                self.nextBoolean = 1
                self.getProjectInfo.updateMeetingLogsTable(self.tempHoldingID, self.meetingType.get(), mergeDates, self.user.get(), mergeDis ,self.sprintID, self.addOrUpdate)
        else:
            if self.meetingDate01.get() != "" and self.meetingDate02.get() != "" and self.meetingDate03.get() != "" and self.spMeetingDisc.get() != "":
                self.nextBoolean = 1
                self.getProjectInfo.updateMeetingLogsTable(self.tempHoldingID, self.meetingType.get(), mergeDates, "", self.spMeetingDisc.get(), self.sprintID, self.addOrUpdate)

    def optionalFrames(self, show):

        if show == "Daily Meeting": #if daily meating
            self.geometry("500x300")

            # Project Name Frame
            frameMid0101 = tk.Frame(self.frameMid01)
            frameMid0101.pack(fill="x")

            lbl1 = tk.Label(frameMid0101, text="Member: ", width=15)
            lbl1.pack(side="left", padx=5, pady=10)
            
            name = tk.StringVar(frameMid0101, value=self.dmuser)
            self.user = tk.Entry(frameMid0101, textvariable=name)
            self.user.pack(fill="x", padx=5, pady=10) # 

            #NEXT SECTION:
            frameMid0102 = tk.Frame(self.frameMid01)
            frameMid0102.pack(fill="x")

            lbl1 = tk.Label(frameMid0102, text="What was done: ", width=15)
            lbl1.pack(side="left", padx=5, pady=10)

            if  self.meeetingID == "":
                name = tk.StringVar(frameMid0102, value=self.sections)
            else:
                name = tk.StringVar(frameMid0102, value=self.sections[0])

            self.dmFirstDisc = tk.Entry(frameMid0102, textvariable=name)
            self.dmFirstDisc.pack(fill="x", padx=5, pady=10) # 

            #NEXT SECTION:
            frameMid0103 = tk.Frame(self.frameMid01)
            frameMid0103.pack(fill="x")

            lbl1 = tk.Label(frameMid0103, text="Obstacules: ", width=15)
            lbl1.pack(side="left", padx=5, pady=10)

            if  self.meeetingID == "":
                name = tk.StringVar(frameMid0103, value=self.sections)
            else:
                name = tk.StringVar(frameMid0103, value=self.sections[1])

            self.dmSecondDisc = tk.Entry(frameMid0103, textvariable=name)
            self.dmSecondDisc.pack(fill="x", padx=5, pady=10) # 

            #NEXT SECTION:
            frameMid0104 = tk.Frame(self.frameMid01)
            frameMid0104.pack(fill="x")

            lbl1 = tk.Label(frameMid0104, text="Next activity to do: ", width=15)
            lbl1.pack(side="left", padx=5, pady=10)

            if  self.meeetingID == "":
                name = tk.StringVar(frameMid0104, value=self.sections)
            else:
                name = tk.StringVar(frameMid0104, value=self.sections[2])

            self.dmThirdDisc = tk.Entry(frameMid0104, textvariable=name)
            self.dmThirdDisc.pack(fill="x", padx=5, pady=10) # 
        else:
            self.geometry("500x200")
            # Project Name Frame
            frame6 = tk.Frame(self.frameMid01)
            frame6.pack(fill="x")

            lbl1 = tk.Label(frame6, text="Summary: ", width=10)
            lbl1.pack(side="left", padx=5, pady=10)

            name = tk.StringVar(frame6, value=self.psmdiscp)
            self.spMeetingDisc = tk.Entry(frame6, textvariable=name)
            self.spMeetingDisc.pack(fill="x", padx=5, pady=10) # 

    def findTheNewIdValues(self):

        dataList = self.getProjectInfo.getGetMeetingLogInputPopup(self.frameOptions, self.meeetingID)
        self.tempHoldingID = dataList[0]

        if self.meeetingID == "":
            self.addOrUpdate = 0
            self.meetingDate01Holder = ["","",""]
            self.sections = ""
            self.dmuser = ""
            self.psmdiscp = ""

            if self.frameOptions != "DMLogs" and self.MeetingSPTyeHolder == "":
                self.MeetingSPTyeHolder = "Sprint Meeting"

        else:
            self.addOrUpdate = 1

            if self.frameOptions == "DMLogs":
                self.meetingDate01Holder = dataList[2].split("/")
                sections = dataList[1]
                self.sections =  sections.split(", SEPERATION01A ")
                sections = dataList[1]
                self.dmuser = dataList[3]
            else:
                self.MeetingSPTyeHolder = dataList[1]
                self.meetingDate01Holder = dataList[3].split("/")
                self.psmdiscp = dataList[2]
        
    def popUpBoxInput(self):
        # Project Name Frame
        self.frameTop = tk.Frame(self)
        self.frameTop.pack(fill="x")

        frameTop01 = tk.Frame(self.frameTop)
        frameTop01.pack(fill="x")


        lbl1 = tk.Label(frameTop01, text="Meeting Type: ", width=15)
        lbl1.pack(side="left", padx=5, pady=10)

        choices = ['Product Backlog Meeting', 'Sprint Meeting', 'Daily Meeting']
        variable = tk.StringVar()
        self.meetingType = ttk.Combobox(frameTop01, textvariable=variable, width=30)
        self.meetingType['values'] = choices
        self.meetingType['state'] = 'readonly' 
        if self.frameOptions == "DMLogs":
            self.meetingType.set('Daily Meeting')
        else:
            self.meetingType.set(self.MeetingSPTyeHolder)
        self.meetingType.bind("<<ComboboxSelected>>", self.clearMidSection)


        #self.meetingType.bind("<<ComboboxSelected>>", onSelected)
        self.meetingType.pack(side="left", padx=5, pady=10) #

        frameTop02 = tk.Frame(self.frameTop)
        frameTop02.pack(fill="x")

        lbl7 = tk.Label(frameTop02, text="Meeting Date: ", width=15)
        lbl7.pack(side="left", padx=5, pady=10)

        name = tk.StringVar(frameTop02, value=self.meetingDate01Holder[0])
        self.meetingDate01 = tk.Entry(frameTop02, textvariable=name, width=5)
        self.meetingDate01.pack(side="left", padx=5, pady=10) #

        lbl8 = tk.Label(frameTop02, text=" / ", width=2)
        lbl8.pack(side="left", padx=5, pady=10)


        name = tk.StringVar(frameTop02, value=self.meetingDate01Holder[1])
        self.meetingDate02 = tk.Entry(frameTop02, textvariable=name, width=5)
        self.meetingDate02.pack(side="left", padx=5, pady=10) 

        lbl9 = tk.Label(frameTop02, text=" / ", width=2)
        lbl9.pack(side="left", padx=5, pady=10)

        name = tk.StringVar(frameTop02, value=self.meetingDate01Holder[2])
        self.meetingDate03 = tk.Entry(frameTop02, textvariable=name, width=10)
        self.meetingDate03.pack(side="left", padx=5, pady=10) 

        frameMid = tk.Frame(self)
        frameMid.pack(fill="x")

        self.frameMid01 = tk.Frame(frameMid)
        self.frameMid01.pack(fill="x")

        botFrame = tk.Frame(self)
        botFrame.pack(fill="x")

        botFrame01 = tk.Frame(botFrame, padx=150)
        botFrame01.pack(anchor="c",fill="x")


        # # Command tells the form what to do when the button is clicked
        self.addButton = tk.Button(botFrame01, text="Submit")
        self.addButton.pack(side= "left", padx=5, pady=10)

        self.deleteButton = tk.Button(botFrame01, text="Delete")
        self.deleteButton.pack(side= "right", padx=5, pady=10)

        if self.frameOptions == "DMLogs":
            self.meetingType.set('Daily Meeting')
            self.optionalFrames("Daily Meeting")
        else:
            self.meetingType.set(self.MeetingSPTyeHolder)
            self.optionalFrames(self.frameOptions)
