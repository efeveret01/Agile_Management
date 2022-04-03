import tkinter as tk
from  tkinter import ttk
from backend import backend

class topSprintNave(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.topFrame = ""
        self.buttomFrame = ""

        self.getProjectInfo = backend()

    def totalProjectRemoval(self, projectID):
        self.getProjectInfo.clearOneWholeProject(projectID)

    def disableAllButtons(self):
        self.Over.configure(state="disable")
        self.gotoProdPage.configure(state="disable")
        self.gotoMeetingPage.configure(state="disable")
        self.delBut.configure(state="disable")
        self.goBack.configure(state="disable") 

    def movingToOverviewPage(self):
        self.Over.configure(state="disable")
        self.gotoProdPage.configure(state="normal")
        self.gotoMeetingPage.configure(state="normal")

    def movingToMeetingPage(self):
        self.Over.configure(state="normal")
        self.gotoProdPage.configure(state="normal")
        self.gotoMeetingPage.configure(state="disable")

    def movingToBacklogPage(self):
        self.Over.configure(state="normal")
        self.gotoProdPage.configure(state="disable")
        self.gotoMeetingPage.configure(state="normal")


    def sprintPage(self,framer):
        projNavDiv = tk.Frame(framer, bd=0, background="white", relief="sunken", height=200, padx=20)
        projNavDiv.pack(fill="x")
        self.buttomFrame = tk.Frame(framer, bd=0, background="white", relief="sunken", height=200, padx=20)
        self.buttomFrame.pack(fill="both", expand="true")


        self.Over = tk.Button(projNavDiv, text="Overview")
        self.gotoProdPage = tk.Button(projNavDiv, text="Product Log")
        self.gotoMeetingPage = tk.Button(projNavDiv, text="Meeting Log")
        self.delBut = tk.Button(projNavDiv, text="DELETE", bg="red", fg='white')
        self.goBack = tk.Button(projNavDiv, text="Back")

        self.Over.pack(side="left")
        self.gotoProdPage.pack(side="left")
        self.gotoMeetingPage.pack(side="left")
        self.goBack.pack(side="right")
        self.delBut.pack(side="right")

        self.movingToOverviewPage()


