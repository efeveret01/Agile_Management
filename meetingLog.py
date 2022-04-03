import tkinter as tk
from  tkinter import ttk
from tkinter.font import Font
from functools import partial
from backend import backend

class meetingLog(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.getProjectInfo = backend()

        self.meeting = ""
        self.sprintID = ""
        self.psmlogButton = ""
        self.dmlogButton = ""
        self.popupBut = ""

    def deleteTableRows(self):
        for i in self.table.get_children():
            self.table.delete(i)

    def TablePopulations(self):
        self.deleteTableRows()

        counter = 0
        if self.meeting == "DMLogs":
            for  numofRows in range(len(self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting))):  # COMPLETED
                print(self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][2])
                

                projectItem = self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][1]
                tempHold = projectItem.split(", SEPERATION01A ")
                look = "WHAT WAS DONE: " + tempHold[0] + ",\n OBSTACLES: " + tempHold[1] + ",\n NEXT ACTIVITY TO DO: " + tempHold[2]

                counter = counter + 1
                self.table.insert(parent='',index='end', text=self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][0], values=(self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][2] , self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][3], look ))
        else:
            for  numofRows in range(len(self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting))):  # COMPLETED
                counter = counter + 1
                self.table.insert(parent='',index='end', text=self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][0], values=(self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][3] , self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][1], self.getProjectInfo.sprintMeetings(self.sprintID, self.meeting)[numofRows][2] ))
            pass
        pass


    def meetingPageSet(self, framer, meeting):
        # Labela nd popup button location
        currPrductDiv = tk.Frame(framer, bd=0, background="white", relief="sunken", height=200, padx=20, pady=20)
        currPrductDiv.pack( fill = "x")

        currSprintLab = tk.Label(currPrductDiv, text="MEETING LOG", font=("Courier", 20), background="white")
        currSprintLab.pack(side="left", fill="x")

        self.addMeetingPopupButton = tk.Button(currPrductDiv, text="Add Meeting")
        self.addMeetingPopupButton.configure(fg="white")
        self.addMeetingPopupButton.configure(bg="#262626")
        self.addMeetingPopupButton.configure(height=2)
        self.addMeetingPopupButton.pack(side="right", fill="x")


        # Changing table buttons
        buttonDiv = tk.Frame(framer, bd=0, background="white", relief="sunken", height=200, padx=20)
        buttonDiv.pack( fill = "x")

        self.spMeetingButton = tk.Button(buttonDiv, text="Sprint/Product Meetings")
        self.spMeetingButton.configure(fg="white")
        self.spMeetingButton.configure(bg="#262626")
        self.spMeetingButton.configure(height=2)
        self.spMeetingButton.pack(side="left", fill="x")

        self.dMeetingButton = tk.Button(buttonDiv, text="Daily Meetings")
        self.dMeetingButton.configure(fg="white")
        self.dMeetingButton.configure(bg="#262626")
        self.dMeetingButton.configure(height=2)
        self.dMeetingButton.pack(side="left", fill="x")
        

        tableFrame = tk.Frame(framer, pady=5)
        tableFrame.pack(fill="x")

        self.table = ttk.Treeview(tableFrame, height=9)
        self.table['show'] = 'headings'
        s = ttk.Style()
        s.configure('Treeview', rowheight=50)   
        
        if meeting == "PSMLogs":
            self.spMeetingButton.configure(state="disable")
            self.dMeetingButton.configure(state="normal")
            self.table['columns'] = ( 'ranks', 'proc_log', 'statues')

            #self.table.column("#0", width=0,  stretch="no")
            self.table.column("ranks",anchor="center", stretch='NO',width=100)
            self.table.column("proc_log",anchor="center", stretch='NO',width=300)
            self.table.column("statues",width=200)

            #self.table.heading("#0",text="",anchor="center")
            self.table.heading("ranks",text="DATE",anchor="center")
            self.table.heading("proc_log",text="MEETING TYPE",anchor="center")
            self.table.heading("statues",text="Summary",anchor="center")
        
        elif meeting == "DMLogs":
            self.dMeetingButton.configure(state="disable")
            self.spMeetingButton.configure(state="normal")
            self.table['columns'] = ( 'ranks', 'proc_log', 'statues')

            #self.table.column("#0", width=0,  stretch="no")
            self.table.column("ranks",anchor="center", stretch='NO',width=100)
            self.table.column("proc_log",anchor="center", stretch='NO',width=300)
            self.table.column("statues",width=200)

            #self.table.heading("#0",text="",anchor="center")
            self.table.heading("ranks",text="DATE",anchor="center")
            self.table.heading("proc_log",text="MEMBER",anchor="center")
            self.table.heading("statues",text="NOTES",anchor="center")
 
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

        self.table.bind('<B1-Motion>', partial(motion_handler, self.table))
        motion_handler(self.table, None)   # Perform initial wrapping
        
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="x")

        self.meeting = meeting
        self.TablePopulations()

