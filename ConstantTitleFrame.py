import tkinter as tk

class ConstantTitleFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

    

    def fixedSections(self, usedFrame):
        #Divide frame
        div2ContentDiv1_1 = tk.Frame(usedFrame, background="white", bd=0, relief="sunken")    #Content div
        div2ContentDiv1_1.grid(row=0, column=0,rowspan=3, columnspan=2, sticky="nsew")

        usedFrame.grid_rowconfigure(0, weight=1)
        usedFrame.grid_columnconfigure(0, weight=10)
        usedFrame.grid_columnconfigure(1, weight=90)

        #Content div seperation
        titleAnadHeaderDiv = tk.Frame(div2ContentDiv1_1, background="white", bd=0, relief="sunken")
        self.pageConetentFrame = tk.Frame(div2ContentDiv1_1, background="white", bd=0, relief="sunken")  # MAIN CONTENT FRAME
        titleAnadHeaderDiv.grid(row=0, column=0,rowspan=1, columnspan=4, sticky="nsew")
        self.pageConetentFrame.grid(row=1, column=0,rowspan=1, columnspan=4, sticky="nsew")
        div2ContentDiv1_1.grid_rowconfigure(0, weight=1)
        div2ContentDiv1_1.grid_rowconfigure(1, weight=99)
        div2ContentDiv1_1.grid_columnconfigure(0, weight=1)


        #ADDING ELEMENTS TO THE TITLE AND HEADER DIV
        titlediv = tk.Frame(titleAnadHeaderDiv, background="white", bd=0, relief="sunken")
        logoutdiv = tk.Frame(titleAnadHeaderDiv, background="white", bd=0, relief="sunken")
        titlediv.grid(row=0, column=0,rowspan=1, columnspan=1, sticky="nsew")
        logoutdiv.grid(row=0, column=1,rowspan=1, columnspan=1, sticky="nsew")
        titleAnadHeaderDiv.grid_columnconfigure(0, weight=1)
        titleAnadHeaderDiv.grid_columnconfigure(0, weight=1)
        
        Label_Title = tk.Label(titlediv, text="IT's PERSONAL")
        Label_Title.configure(bg="white")
        Label_Title.configure(font="-family {Segoe UI} -size 15 -weight bold -slant roman -underline 0 -overstrike 0")
        Label_Title.configure(foreground="black")
        Label_Title.pack(side="top", anchor='nw')
