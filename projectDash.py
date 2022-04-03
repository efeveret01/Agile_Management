import tkinter as tk
from  tkinter import ttk
from tkinter.font import Font
from functools import partial
from backend import backend

class projectDash(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.getProjectInfo = backend()

    def preventActionClickes(self):
        self.completeButton.configure(state="disable")
        self.getInputButton.configure(state="disable")
        self.table.unbind("<Button 1>")
        pass
    
    def populateTheTable(self, completeOrNot): # "c" (completed) or "a" (active)
        counter = 0
        for  numofRows in range(len(self.getProjectInfo.getAllProjects())):  # COMPLETED
            if self.getProjectInfo.getAllProjects()[numofRows][5] == completeOrNot:
                counter = counter + 1
                self.table.insert(parent='',index='end',iid=self.getProjectInfo.getAllProjects()[numofRows][0], text=self.getProjectInfo.getAllProjects()[numofRows][0], values=(counter , self.getProjectInfo.getAllProjects()[numofRows][1], self.getProjectInfo.getAllProjects()[numofRows][2] ))
        pass

    def activeButtonWasClicked(self):
        self.deleteTableRows()
        self.populateTheTable("a")

        self.activeButton.configure(state="disable")
        self.activeButton.configure(bg="gray")
        self.completeButton.configure(state="normal")

    def completeButtonWasClicked(self):
        self.deleteTableRows()
        self.populateTheTable("c")
        
        self.completeButton.configure(state="disable")
        self.completeButton.configure(bg="gray")
        self.activeButton.configure(state="normal")
        self.activeButton.configure(bg="#262626")

    def addProjectButtonWasClicked(self):
        self.getInputButton.configure(state="disable")
        self.getInputButton.configure(bg="gray")
        self.completeButton.configure(state="disable")
        self.getInputButton.configure(state="disable")

    def deleteTableRows(self):
        for i in self.table.get_children():
            self.table.delete(i)

    def overallContent(self, framer):
        pageNav = tk.Frame(framer, bd=0, relief="sunken")
        mainCont = tk.Frame(framer, background="white", bd=0, relief="sunken")
        pageNav.grid(row=0, column=0,rowspan=1, columnspan=1, sticky="nsew")
        mainCont.grid(row=1, column=0,rowspan=1, columnspan=1, sticky="nsew")
        framer.grid_rowconfigure(0, weight=1)
        framer.grid_rowconfigure(1, weight=99)
        framer.grid_columnconfigure(0, weight=1)  

        #content nav
        timePNav1 = tk.Frame(pageNav, background="white", bd=0, relief="sunken")
        timePNav2 = tk.Frame(pageNav, background="white", bd=0, relief="sunken")
        timePNav3 = tk.Frame(pageNav, background="white", bd=0, padx=20, relief="sunken")
        timePNav4 = tk.Frame(pageNav, background="white", bd=0, relief="sunken")
        timePNav1.grid(row=0, column=0,rowspan=1, columnspan=1, sticky="nsew")
        timePNav2.grid(row=0, column=1,rowspan=1, columnspan=1, sticky="nsew")
        timePNav3.grid(row=0, column=2,rowspan=1, columnspan=1, sticky="nsew")
        timePNav4.grid(row=0, column=3,rowspan=1, columnspan=1, sticky="nsew")

        pageNav.grid_columnconfigure(0, weight=0)
        pageNav.grid_columnconfigure(1, weight=0)
        pageNav.grid_columnconfigure(2, weight=1)
        pageNav.grid_columnconfigure(3, weight=20)

        #Seperating main content
        timePTop1 = tk.Frame(mainCont, background="white", bd=0, relief="sunken", pady=20, padx=20)
        timePTable2 = tk.Frame(mainCont, background="white", bd=0, relief="sunken", padx=20, pady=20)
        timePTop1.grid(row=0, column=0,rowspan=1, columnspan=1, sticky="nsew")
        timePTable2.grid(row=1, column=0,rowspan=1, columnspan=1, sticky="nsew")

        mainCont.grid_rowconfigure(0, weight=1)
        mainCont.grid_rowconfigure(1, weight=20)
        mainCont.grid_columnconfigure(0, weight=1)  
        
        #top buttons for table
        tableButton1 = tk.Frame(timePTop1, background="white", bd=0, relief="sunken")
        tableButton2 = tk.Frame(timePTop1, background="white", bd=0, relief="sunken")
        tableButton3 = tk.Frame(timePTop1, background="white", bd=0, relief="sunken")
        tableButton1.grid(row=0, column=0,rowspan=1, columnspan=1, sticky="nsew")
        tableButton2.grid(row=0, column=1,rowspan=1, columnspan=1, sticky="nsew")
        tableButton3.grid(row=0, column=2,rowspan=1, columnspan=1, sticky="nsew")


        timePTop1.grid_columnconfigure(0, weight=1)
        timePTop1.grid_columnconfigure(1, weight=1)
        timePTop1.grid_columnconfigure(2, weight=20)


        contentProjectTab = tk.Label(timePNav3, text="PROJECTS")
        contentProjectTab.configure(bg="white")
        contentProjectTab.configure(font="-family {Segoe UI} -size 15 -weight bold -slant roman -underline 0 -overstrike 0")
        contentProjectTab.configure(foreground="black")
        contentProjectTab.pack(side="top", anchor='nw')

        # Frame Buttons
        self.activeButton = tk.Button(tableButton1, text="Active")
        self.activeButton.configure(fg="white")
        self.activeButton.configure(bg="gray")
        self.activeButton.configure(state="disable") 
        self.activeButton.configure(height=2)
        self.activeButton.pack(side="top", fill="x")

        self.completeButton = tk.Button(tableButton2, text="Completed")
        self.completeButton.configure(fg="white")
        self.completeButton.configure(bg="#262626")
        self.completeButton.configure(height=2)
        self.completeButton.pack(side="top", fill="x")

        self.getInputButton = tk.Button(tableButton3, text="Add Project")
        self.getInputButton.configure(fg="white")
        self.getInputButton.configure(bg="#262626")
        self.getInputButton.configure(height=2)
        self.getInputButton.pack(side="right", fill="x")

        # Frame table
        tableFrame = tk.Frame(timePTable2)
        tableFrame.pack(fill="x")

        self.table = ttk.Treeview(tableFrame, height=9)
        self.table['show'] = 'headings'
        s = ttk.Style()
        s.configure('Treeview', rowheight=50)   

        self.table['columns'] = ('num', 'project_name', 'project_disc')

        self.table.column("num",anchor='center', stretch='NO', width=50)
        self.table.column("project_name", stretch='NO', width=300)
        self.table.column("project_disc",width=50)


        self.table.heading("num",text="No.",anchor='center')
        self.table.heading("project_name",text="PROJECT NAME",anchor='center')
        self.table.heading("project_disc",text="DESCRIPTION",anchor='center')

        

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



        self.table.pack(fill="both", expand="true")
        
        # Populate table
        self.activeButtonWasClicked()
      
