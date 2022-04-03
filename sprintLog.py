#from struct import pack
import tkinter as tk
from  tkinter import ttk
from tkinter.font import Font
from functools import partial
from turtle import right

from click import command

from backend import backend

class sprintLog(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.getProjectInfo = backend()
        
        self.setProjectID =""
        self.gottenSprintID = ""
        self.gottenSprintNum = ""
        self.gottenCurrentSprintNum = ""
        self.popupBut = ""
        self.arr = []

    def completeTheProject(self, id):
        self.getProjectInfo.completeTheProject(id)

    def clearContentFrame(self):
        for widget in self.sprintMainFrame.winfo_children():
            widget.destroy()

    def testprint(self, event):
        self.clearContentFrame()
        self.sprintPage(self.sprintMainFrame, self.setProjectID, str(event))

    def populateTheTable(self): # "c" or "a"
        projectItem = ""
        ntStarted = ""
        wip = ""
        completed = ""

        for  numofRows in range(len(self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID))):  # COMPLETED
            ntStarted = ""
            wip = ""
            completed = ""
            if projectItem != self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][1]:
                projectItem = self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][1]
                tempHold = projectItem.split(", SEPERATION01A ")
                look = "As a user, " + tempHold[0] + ", so I can " + tempHold[1]

                if self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][3] == "Not Started":
                    ntStarted ="X"
                elif self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][3] == "W.I.P":
                    wip = "X"
                else:
                    completed = "X"

                self.bLtable.insert(parent='',index='end', text=self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][0], values=(look, self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][2], ntStarted, wip, completed ))
            else:
                #put inside without value ""
                if self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][3] == "Not Started":
                    ntStarted ="X"
                elif self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][3] == "W.I.P":
                    wip = "X"
                else:
                    completed = "X"
                self.bLtable.insert(parent='',index='end', text=self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][0], values=("", self.getProjectInfo.populateSprintItemTablePage(self.gottenSprintID)[numofRows][2], ntStarted, wip, completed ))

    def populateTheInputBox(self):
        tempSprintMAXNumber, tempSprintID =  self.getProjectInfo.getDesiredSprint(self.setProjectID, self.gottenCurrentSprintNum)

        if self.gottenCurrentSprintNum == "":
            self.gottenCurrentSprintNum = tempSprintMAXNumber

        self.setProjectID = self.setProjectID
        self.gottenSprintID = tempSprintID
        self.gottenSprintNum = tempSprintMAXNumber

        projInfo =  self.getProjectInfo.getProjectIDForProjectInputPopup(self.setProjectID)

        self.contName.configure(text=projInfo[1])
        self.contsdate.configure(text="Starting Date: " + projInfo[3])
        self.contedate.configure(text="Ending Date: " + projInfo[4])
        self.contdisc.configure(text="Descriptions: \n " + projInfo[2])
        self.currSprintLab.configure(text="SPRINT No " + self.gottenCurrentSprintNum)

        for x in range(1,(int(tempSprintMAXNumber)+1)):
            if x == int(self.gottenCurrentSprintNum):
                haha = "Sprint " + str(x)
                tempBTN = tk.Button(self.NavButtonSection, bd= 5, text=haha, state="disable")
                #tempBTN.configure(command= self.testprint)
                #tempBTN.bind('<Button-1>', self.testprint)
                tempBTN.pack(side="left", anchor="center")
                self.arr.append(tempBTN)
                

            else:
                haha = "Sprint " + str(x)
                tempBTN = tk.Button(self.NavButtonSection, bd= 5, text=haha)  # , command=lambda m=str(x): self.testprint(m)
                tempBTN.pack(side="left", anchor="center")
                self.arr.append(tempBTN)
                #tempBTN.pack(side="left", anchor="center")
        
        if projInfo[5] == "a":
            self.completeButton.pack(side= "left", padx=5, pady=10)
            if self.gottenCurrentSprintNum == self.gottenSprintNum:
                self.NextSprButton.pack(side= "right", padx=5, pady=10)
        else:
            x = self.contName['text']
            x = x + " - COMPLETED"
            self.contName.configure(text=x)

    def sprintPage(self, framer):
        self.sprintMainFrame = framer

        self.frame = tk.Frame(self.sprintMainFrame, bd=2, relief="sunken", height=200, padx=20, pady=10)
        self.frame.pack( fill="x")

        NameAndDateFrame = tk.Frame(self.frame)
        NameAndDateFrame.pack( fill="x")
        
        self.contName = tk.Label(NameAndDateFrame, font=("Courier", 44))
        self.contName.pack(side="left")

        self.contsdate = tk.Label(NameAndDateFrame)
        self.contsdate.pack(anchor="ne" )
        
        self.contedate = tk.Label(NameAndDateFrame)
        self.contedate.pack(anchor="ne" )
        
        discSection = tk.Frame(self.frame)
        discSection.pack( fill="x")
        
        self.contdisc = tk.Label(discSection)
        self.contdisc.pack(side= "left", anchor="w")


        # 2 frame section
        buttonsSection = tk.Frame(self.sprintMainFrame, bd=0, background="white", relief="sunken", height=200, padx=20, pady=20)
        buttonsSection.pack( fill="x")
        self.currSprintLab = tk.Label(buttonsSection, font=("Courier", 20), background="white")
        self.currSprintLab.pack(side="left")
        
        self.addSprintPopupButton = tk.Button(buttonsSection, text="Add Sprint Item")
        self.addSprintPopupButton.configure(fg="white")
        self.addSprintPopupButton.configure(bg="#262626")
        self.addSprintPopupButton.configure(height=2)
        self.addSprintPopupButton.pack(side="right", fill="x")

        # 1 frame section
        self.NavButtonSection = tk.Frame(self.sprintMainFrame, bd=0, background="white", relief="sunken", height=200, padx=20, pady=5)
        self.NavButtonSection.pack(fill="x")
        
        
        # 1 frame section
        tableFrame = tk.Frame(self.sprintMainFrame)
        tableFrame.pack(fill="x")
        
        self.bLtable = ttk.Treeview(tableFrame, height=7)
        self.bLtable['show'] = 'headings'
        s = ttk.Style()
        s.configure('Treeview', rowheight=50)   

        self.bLtable['columns'] = ('SprintLog', 'sprint_item', 'spr_InProgress', 'spr_ReadyTest', 'spr_Completed')

        self.bLtable.column("SprintLog", width=200)
        self.bLtable.column("sprint_item",width=200)
        self.bLtable.column("spr_InProgress",anchor="center", stretch='NO', width=150)
        self.bLtable.column("spr_ReadyTest",anchor="center", stretch='NO', width=150)
        self.bLtable.column("spr_Completed",anchor="center", width=150)

        self.bLtable.heading("SprintLog",text="Product Backlog Item",anchor="center")
        self.bLtable.heading("sprint_item",text="Sprint Item",anchor="center")
        self.bLtable.heading("spr_InProgress",text="Not Started",anchor="center")
        self.bLtable.heading("spr_ReadyTest",text="Work In Progress",anchor="center")
        self.bLtable.heading("spr_Completed",text="Completed",anchor="center")

        def motion_handler(tree, event):
            f = Font(font='TkDefaultFont')
            # A helper function that will wrap a given value based on column width
            def adjust_newlines(val, width, pad=10):
                if not isinstance(val, str):
                    return val
                else:
                    words = val.split()
                    lines = [[],]
                    for word in words:
                        line = lines[-1] + [word,]
                        if f.measure(' '.join(line)) < (width - pad):
                            lines[-1].append(word)
                        else:
                            lines[-1] = ' '.join(lines[-1])
                            lines.append([word,])

                    if isinstance(lines[-1], list):
                        lines[-1] = ' '.join(lines[-1])

                    return '\n'.join(lines)

            if (event is None) or (tree.identify_region(event.x, event.y) == "separator"):
                # You may be able to use this to only adjust the two columns that you care about
                # print(tree.identify_column(event.x))

                col_widths = [tree.column(cid)['width'] for cid in tree['columns']]

                for iid in tree.get_children():
                    new_vals = []
                    for (v,w) in zip(tree.item(iid)['values'], col_widths):
                        new_vals.append(adjust_newlines(v, w))
                    tree.item(iid, values=new_vals)

        self.bLtable.bind('<B1-Motion>', partial(motion_handler, self.bLtable))
        motion_handler(self.bLtable, None)   # Perform initial wrapping

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.bLtable.yview)
        self.bLtable.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.bLtable.pack(fill="x")
        
        # 1 frame section
        buttomSection = tk.Frame(self.sprintMainFrame, bd=0, background="white", relief="sunken", height=200, padx=20, pady=5)
        buttomSection.pack(anchor="s", fill="both", expand="true")
        self.completeButton = tk.Button(buttomSection, text="Complete Project")
        self.NextSprButton = tk.Button(buttomSection, text="Next Sprint")
        
