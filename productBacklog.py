import tkinter as tk
from  tkinter import ttk
from tkinter.font import Font
from functools import partial
from backend import backend

class productBacklog(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.getProjectInfo = backend()

        self.addProdIt = ""
        self.ProjectID = ""


    def populateTheTable(self): # "c" or "a"
        #counter = 0
        for  numofRows in range(len(self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID))):  # COMPLETED
            projectItem = self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID)[numofRows][2]
            tempHold = projectItem.split(", SEPERATION01A ")
            look = "As a user, " + tempHold[0] + ", so I can " + tempHold[1]
            self.bLtable.insert(parent='',index='end',iid=self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID)[numofRows][0], text=self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID)[numofRows][0], values=(self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID)[numofRows][1] , look, self.getProjectInfo.populateProductBacklogTablePage(self.ProjectID)[numofRows][3] ))

    def productBackPage(self, framer):
        # Page label and buttons
        currPrductDiv = tk.Frame(framer, bd=0, background="white", relief="sunken", height=200, padx=20, pady=20)
        currPrductDiv.pack(fill = "x")
        
        currSprintLab = tk.Label(currPrductDiv, text="PRODUCT LOG", font=("Courier", 20), background="white")
        currSprintLab.pack(side="left")

        self.addProjItemButton = tk.Button(currPrductDiv, text="Add Product Items")
        self.addProjItemButton.configure(fg="white")
        self.addProjItemButton.configure(bg="#262626")
        self.addProjItemButton.configure(height=2)
        self.addProjItemButton.pack(side="right", fill="x")

        # Page table
        tableFrame = tk.Frame(framer)
        tableFrame.pack(fill="x")

        self.bLtable = ttk.Treeview(tableFrame, height=9)
        self.bLtable['show'] = 'headings'
        s = ttk.Style()
        s.configure('Treeview', rowheight=50)   

        self.bLtable['columns'] = ('pri', 'item', 'stat')

        #self.bLtable.column("#0", width=0,  stretch="no")
        self.bLtable.column("pri",anchor="center", stretch='NO', width=100)
        self.bLtable.column("item",width=200)
        self.bLtable.column("stat",anchor="center",width=70)


        #self.bLtable.heading("#0",text="",anchor="center")
        self.bLtable.heading("pri",text="Priority",anchor="center")
        self.bLtable.heading("item",text="Product Item",anchor="center")
        self.bLtable.heading("stat",text="Status",anchor="center")

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
