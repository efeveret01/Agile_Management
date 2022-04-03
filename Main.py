import tkinter as tk
from tkinter import ttk

from click import command

from ConstantTitleFrame import ConstantTitleFrame
from projectDash import projectDash

from projectInputNameBox import projectInputNameBox
from inputMeetingPopup import inputMeetingPopup
from inputSprintItemPopup import inputSprintItemPopup
from projBacklogInputBox import projBacklogInputBox

from topSprintNave import topSprintNave
from sprintLog import sprintLog
from productBacklog import productBacklog
from meetingLog import meetingLog


import sys

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IT's PERSONAL: Project")
        self.geometry("1200x800+150+30") #Width Hight x-position y-position
        self.protocol("WM_DELETE_WINDOW", self.ultimateClose)

        self.subContent1 = tk.Frame()

        self.setProjectID = ""
        self.setProjectItemID = ""
        self.setTotalSprintNum = ""
        self.setCurrentSprintNum = ""
        self.sprntID = ""
        self.selectedMeetingTab = "PSMLogs"
        self.sprintItemID = ""
        self.meeetingID = ""
        self.frameOptions = "Daily Meeting"
        self.headerClicked = 0

    # WHEN MAIN FRAME IS CLOSED, CLOSE ALL
    def ultimateClose(self):
        sys.exit()

    # STOP TABLE HEADER FROM ACTIONS
    def headerWasClicked(self):
        self.headerClicked = 1

    # CLEAR FUNCTION FOR CONTENT FRAME
    def clearSubContentFrame(self):
        for widget in self.subContent1.winfo_children():
                    widget.destroy()

    ########################################################
    # PRODUCT BACKLOG ITEMS POPUP INPUT BOX  - [COMPLETE]
    ########################################################
    def openProductBacklogItemPopupBox(self):
        
        #Button actions
        def on_closing():
            self.setProjectItemID = ""
            popup.closeWindow()
            self.clearSubContentFrame()
            self.movingToProductBacklogPage()
        
        def clickAddButtonToAdd():
            popup.addTheProductItemsToDatabase()
            if popup.nextBoolean == 1:
                self.setProjectItemID = ""
                popup.closeWindow()
                self.clearSubContentFrame()
                self.movingToProductBacklogPage()

        def deleteTheProductItemsToDatabase():
            popup.deleteTheProductItemsToDatabase()
            self.setProjectItemID = ""
            popup.closeWindow()
            self.clearSubContentFrame()
            self.movingToProductBacklogPage()
        
        #Setup popup box
        popup = projBacklogInputBox()
        popup.popUpBoxInput(self.setProjectItemID, self.setProjectID)

        #Configure buttons
        popup.submitButton.configure(command=clickAddButtonToAdd)
        popup.deleteButton.configure(command= deleteTheProductItemsToDatabase)
        popup.protocol("WM_DELETE_WINDOW", on_closing)

        popup.mainloop()

    ########################################################
    # CREATE PRODUCT BACKLOG PAGE  - [COMPLETE]
    ########################################################
    def movingToProductBacklogPage(self):
        
        #Button actions
        def OnDoubleClick(event):
            if self.headerClicked == 0 and pPageButtom.bLtable.item(pPageButtom.bLtable.focus())['text'] != "":
                pPageTop.disableAllButtons()
                pPageButtom.bLtable.unbind("<Double-1>")
                pPageButtom.addProjItemButton.configure(state="disable")
                self.setProjectItemID = pPageButtom.bLtable.item(pPageButtom.bLtable.focus())['text']
                print(self.setProjectItemID)
                self.openProductBacklogItemPopupBox()
            self.headerClicked = 0

        def deleteProject():
            pPageTop.totalProjectRemoval(self.setProjectID)
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()

        def movingToTheMeetingPage():
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()

        def movingToOverviewPage():
            self.clearSubContentFrame()
            self.movingToSprintPage()

        def backToMainPage():
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()

        def activateProductItemPopup():
            pPageTop.disableAllButtons()
            pPageButtom.bLtable.unbind("<Double-1>")
            pPageButtom.addProjItemButton.configure(state="disable")
            self.openProductBacklogItemPopupBox()

        #Set top section
        pPageTop = topSprintNave()
        pPageTop.sprintPage(self.subContent1)
        pPageTop.movingToBacklogPage()
        prdLogPage = pPageTop.buttomFrame

        #configure buttons
        pPageTop.Over.configure(command=movingToOverviewPage)
        pPageTop.gotoMeetingPage.configure(command=movingToTheMeetingPage)
        pPageTop.goBack.configure(command=backToMainPage)
        pPageTop.delBut.configure(command=deleteProject)
        
        #Set product backlog section
        pPageButtom = productBacklog()
        pPageButtom.productBackPage(prdLogPage)
        pPageButtom.ProjectID = self.setProjectID 

        #configure buttons and table
        pPageButtom.bLtable.bind("<Double-1>", OnDoubleClick)
        pPageButtom.populateTheTable()
        pPageButtom.addProjItemButton.configure(command=activateProductItemPopup)

    ########################################################
    # MEETING LOG POPUP INPUT BOX  - [COMPLETE]
    ########################################################
    def openMeetingLogPopupBox(self):
        
        #Button actions
        def closingPopup():
            self.meeetingID = ""
            popup.closeWindow()
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()

        def addOrUpdateButton():
            popup.pushDataintoDatabase()
            if popup.nextBoolean == 1:
                self.meeetingID = ""
                popup.closeWindow()
                self.clearSubContentFrame()
                self.movingToMeetingLogPage()
        
        def clearBotFrame():
            self.meeetingID = ""
            popup.deleteMeetingLog()
            popup.clearBotFrame()
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()
        
        #Setup popup box
        popup = inputMeetingPopup()
        popup.sprintID = self.sprntID
        popup.meeetingID = self.meeetingID
        popup.frameOptions = self.selectedMeetingTab
        popup.findTheNewIdValues()
        popup.popUpBoxInput()

        #Configure buttons
        if self.meeetingID != "":
            popup.meetingType.configure(state="disable")

        popup.addButton.configure(command=addOrUpdateButton)
        popup.deleteButton.configure(command= clearBotFrame)
        popup.protocol("WM_DELETE_WINDOW", closingPopup)

        popup.mainloop()

    ########################################################
    # CREATE MEETING PAGE  - [COMPLETE]
    ########################################################
    def movingToMeetingLogPage(self):

        #Button actions
        def OnDoubleClick(event):
            if self.headerClicked == 0 and pPageButtom.table.item(pPageButtom.table.focus())['text'] != "":
                pPageTop.disableAllButtons()
                pPageButtom.table.unbind("<Double-1>")
                pPageButtom.addMeetingPopupButton.configure(state="disable")
                pPageButtom.spMeetingButton.configure(state="disable")
                pPageButtom.dMeetingButton.configure(state="disable")

                self.meeetingID =   pPageButtom.table.item(pPageButtom.table.focus())['text']
                self.openMeetingLogPopupBox()
            self.headerClicked = 0
        
        def deleteProject():
            pPageTop.totalProjectRemoval(self.setProjectID)
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()

        def movingToTheProductLogPage():
            self.clearSubContentFrame()
            self.movingToProductBacklogPage()

        def movingToOverviewPage():
            self.clearSubContentFrame()
            self.movingToSprintPage()

        def backToMainPage():
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()

        def activateMeetingPopup():
            pPageTop.disableAllButtons()
            pPageButtom.table.unbind("<Double-1>")
            pPageButtom.addMeetingPopupButton.configure(state="disable")
            pPageButtom.spMeetingButton.configure(state="disable")
            pPageButtom.dMeetingButton.configure(state="disable")

            self.openMeetingLogPopupBox()

        def selectSPMeetingTab():
            self.selectedMeetingTab = "PSMLogs"
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()

        def selectDailyMeetingTab():
            self.selectedMeetingTab = "DMLogs"
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()

        #Set top section
        pPageTop = topSprintNave()
        pPageTop.sprintPage(self.subContent1)
        pPageTop.movingToMeetingPage()
        meetPage = pPageTop.buttomFrame

        #configure buttons
        pPageTop.gotoProdPage.configure(command=movingToTheProductLogPage)
        pPageTop.Over.configure(command=movingToOverviewPage)
        pPageTop.goBack.configure(command=backToMainPage)
        pPageTop.delBut.configure(command=deleteProject)

        #set Meeting page
        pPageButtom = meetingLog()
        pPageButtom.sprintID = self.sprntID
        pPageButtom.meetingPageSet(meetPage, self.selectedMeetingTab)

        #configure buttons and table
        pPageButtom.addMeetingPopupButton.configure(command=activateMeetingPopup)
        pPageButtom.spMeetingButton.configure(command=selectSPMeetingTab)
        pPageButtom.dMeetingButton.configure(command=selectDailyMeetingTab)
        pPageButtom.table.bind("<Double-1>", OnDoubleClick)

    ########################################################
    # SPRINT POPUP INPUT BOX  - [COMPLETE]
    ########################################################
    def openSprintItemPopupBox(self, path):
        #Button actions
        def closeWindow():
            popup.closeWindow()
            self.clearSubContentFrame()
            self.movingToSprintPage()

        #Activate and populate popup box
        popup = inputSprintItemPopup()
        popup.projectID = self.setProjectID
        popup.sprintID = self.sprntID
        popup.sprintItemID = self.sprintItemID

        if path == "add":
            popup.hidOption = 1
        
        popup.popUpBoxInput()
        popup.protocol("WM_DELETE_WINDOW", closeWindow)
        popup.mainloop()

    ########################################################
    # CREATE SPRINT PAGE  - [COMPLETE]
    ########################################################
    def movingToSprintPage(self):

        #Page functions
        def disableTypeA():
            for widget in pPageButtom.frame.winfo_children():
                widget.unbind("<Double-1>")
            pPageButtom.contName.unbind("<Double-1>")
            pPageButtom.contsdate.unbind("<Double-1>")
            pPageButtom.contedate.unbind("<Double-1>")
            pPageButtom.contdisc.unbind("<Double-1>")
            pPageTop.disableAllButtons()
            for x in range(len(pPageButtom.arr)):
                pPageButtom.arr[x].configure(state="disable")
            pPageButtom.bLtable.unbind("<Double-1>")
            pPageButtom.addSprintPopupButton.configure(state="disable")
            pPageButtom.completeButton.configure(state="disable")
            pPageButtom.NextSprButton.configure(state="disable")

        #Button actions
        def OnDoubleClick(event):
            if self.headerClicked == 0 and pPageButtom.bLtable.item(pPageButtom.bLtable.focus())['text'] != "":
                disableTypeA()
                self.sprintItemID = pPageButtom.bLtable.item(pPageButtom.bLtable.focus())['text']
                self.openSprintItemPopupBox("add")
            self.headerClicked = 0

        def OnDoubleClickOpenPopUpProject(event):
            disableTypeA()
            self.openProjectInputPopupBox()

        def testpress(event):
            self.setCurrentSprintNum = str( int(event) + 1 )
            self.clearSubContentFrame()
            self.movingToSprintPage()

        def deleteProject():
            pPageTop.totalProjectRemoval(self.setProjectID)
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()

        def backToMainPage():
            self.setProjectID = ""
            self.setTotalSprintNum = ""
            self.setCurrentSprintNum = ""
            self.startMainProjectPage()
        
        def movingToTheMeetingPage():
            self.clearSubContentFrame()
            self.movingToMeetingLogPage()

        def movingToTheProductLogPage():
            self.clearSubContentFrame()
            self.movingToProductBacklogPage()

        def moveToNextSprint():
            self.setCurrentSprintNum = str(int(self.setCurrentSprintNum) + 1)
            self.clearSubContentFrame()
            self.movingToSprintPage()

        def completeTheProject():
            pPageButtom.completeTheProject(self.setProjectID)
            backToMainPage()

        def activateSprintPopup():
            disableTypeA()
            self.openSprintItemPopupBox("")

        # top frame: Set
        pPageTop = topSprintNave()
        pPageTop.sprintPage(self.subContent1)

        # top frame: Button configured
        pPageTop.gotoProdPage.configure(command=movingToTheProductLogPage)
        pPageTop.gotoMeetingPage.configure(command=movingToTheMeetingPage)
        pPageTop.goBack.configure(command=backToMainPage)
        pPageTop.delBut.configure(command=deleteProject)

        # buttom frame: Set
        sprintPg = pPageTop.buttomFrame
        pPageButtom = sprintLog()
        pPageButtom.setProjectID = self.setProjectID
        pPageButtom.gottenCurrentSprintNum = self.setCurrentSprintNum
        pPageButtom.sprintPage(sprintPg)
        pPageButtom.populateTheInputBox()
        pPageButtom.populateTheTable()
        self.sprntID = pPageButtom.gottenSprintID

        # Navigation buttons configure
        for x in range(len(pPageButtom.arr)):
            pPageButtom.arr[x].configure(command=lambda m=str(x): testpress(m))

        # Get current sprint
        self.setCurrentSprintNum = pPageButtom.gottenCurrentSprintNum
        
        # get and set page buttons with actions
        for widget in pPageButtom.frame.winfo_children():
                    widget.bind("<Double-1>", OnDoubleClickOpenPopUpProject)
        pPageButtom.contName.bind("<Double-1>", OnDoubleClickOpenPopUpProject)
        pPageButtom.contsdate.bind("<Double-1>", OnDoubleClickOpenPopUpProject)
        pPageButtom.contedate.bind("<Double-1>", OnDoubleClickOpenPopUpProject)
        pPageButtom.contdisc.bind("<Double-1>", OnDoubleClickOpenPopUpProject)
        
        pPageButtom.bLtable.bind("<Double-1>", OnDoubleClick)
        
        pPageButtom.addSprintPopupButton.configure(command=activateSprintPopup)
        pPageButtom.completeButton.configure(command=completeTheProject)
        pPageButtom.NextSprButton.configure(command=moveToNextSprint)

    ########################################################
    # PROJECT POPUP INPUT BOX  - [COMPLETED]
    ########################################################
    def openProjectInputPopupBox(self):
        # button actions:
        def onClosingInput():
            getMainContent.on_closing()
            if self.setProjectID == "":
                self.startMainProjectPage()
            else:
                self.clearSubContentFrame()
                self.movingToSprintPage()

        def makeSubmitAdd():
            getMainContent.addNewProject()
            self.setProjectID = getMainContent.projectID
            getMainContent.on_closing()
            self.clearSubContentFrame()
            self.movingToSprintPage()

        def makeSubmitUpdate():
            getMainContent.updateProject()
            getMainContent.on_closing()
            self.clearSubContentFrame()
            self.movingToSprintPage()

        #Acitvate popup window
        getMainContent = projectInputNameBox()
        getMainContent.projectID = self.setProjectID
        getMainContent.popUpBoxInput()

        getMainContent.protocol("WM_DELETE_WINDOW", onClosingInput)

        #Configure buttons
        if self.setProjectID == "":
            getMainContent.submitButton.configure(command= makeSubmitAdd)
            getMainContent.getProjectsDataUsingProjectID()
        else:
            getMainContent.submitButton.configure(command= makeSubmitUpdate)
            getMainContent.getProjectsDataUsingProjectID()

        getMainContent.mainloop()


    ########################################################
    # SET MAIN PAGE  - [COMPLETE]
    ########################################################
    def startMainProjectPage(self):
        # reset content frame
        self.clearSubContentFrame()

        # quick content frame populator:
        def populateFrame():
            getMainContent.overallContent(self.subContent1)
            getMainContent.activeButton.configure(command= whenActiveIsClicked)
            getMainContent.completeButton.configure(command= whenCompleteIsClicked)
            getMainContent.getInputButton.configure(command= whenAddProjectButtonIsClicked)
            getMainContent.table.heading("num", command=lambda : self.headerWasClicked())
            getMainContent.table.heading("project_name", command=lambda : self.headerWasClicked())
            getMainContent.table.heading("project_disc", command=lambda : self.headerWasClicked())
            getMainContent.table.bind("<Double-1>", OnDoubleClick)

        # button actions:
        def OnDoubleClick(event):
            if self.headerClicked == 0 and getMainContent.table.item(getMainContent.table.focus())['text'] != "":
                self.setProjectID = str(getMainContent.table.item(getMainContent.table.focus())['text'])
                self.clearSubContentFrame()
                self.movingToSprintPage()
            self.headerClicked = 0

        def whenActiveIsClicked():
            self.clearSubContentFrame()
            populateFrame()
            getMainContent.activeButtonWasClicked()

        def whenCompleteIsClicked():
            self.clearSubContentFrame()
            populateFrame()
            getMainContent.completeButtonWasClicked()

        def whenAddProjectButtonIsClicked():
            getMainContent.table.unbind("<Double-1>")
            getMainContent.addProjectButtonWasClicked()
            self.openProjectInputPopupBox()

        # Visualize and Populate root and Sub Content Fames
        getMainPage = ConstantTitleFrame()
        getMainPage.fixedSections(self)
        self.subContent1 = getMainPage.pageConetentFrame

        getMainContent = projectDash()
        getMainContent.overallContent(self.subContent1)
        populateFrame()


if __name__ == "__main__":
    startMain = MainView()
    startMain.startMainProjectPage()
    startMain.mainloop()



