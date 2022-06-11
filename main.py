import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk
from functions import files as f
from functions import database as db


class MainApp: # Main class
    def __init__(self, master):
        # App configuration
        self.master = master
        self.master.title("Data Updater")
        try:
            self.master.iconbitmap("./data/logo.ico")
        except: # In linux didn't work
            print("Logo not working (maybe it's your operational system, like Linux)")

        self.screenSizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()]
        self.appSizes = [400, 400, 100, 100] # Width, Height, initialX, initialY

        self.master.geometry(f"{self.appSizes[0]}x{self.appSizes[1]}+{self.appSizes[2]}+{self.appSizes[3]}")

        # Database filename
        try:
            self.db = db.getDatabase("Database")
        except: # Create database of filename
            db.createDatabase("Database", {"Filename": "TEXT"})
            db.addToDatabase("Database", "Filename", ("./database.xls", ))

        self.db = db.getDatabase("Database")["Filename"].values[0]

        # Database selector
        self.dbLabel = Label(self.master, text=self.db)
        self.dbLabel.pack()
        self.dbLabel.place(bordermode=OUTSIDE, relheight=.05, relwidth=.3, relx=.65, rely=.8, anchor="nw")

        self.dbDefiner = Button(self.master, text="Change DB", command=lambda: f.fileSelect([("Excel files", ".xls")], self.changeDB))
        self.dbDefiner.pack()
        self.dbDefiner.place(bordermode=OUTSIDE, relheight=.1, relwidth=.3, relx=.65, rely=.85, anchor="nw")

        # Database List
        self.dbFrame = Frame(self.master)
        self.dbFrame.pack()
        self.dbFrame.place(bordermode=OUTSIDE, relheight=.7, relwidth=.8, relx=.1, rely=.05, anchor="nw")

        self.tree = ttk.Treeview(self.dbFrame)
        self.tree.place(relheight=1, relwidth=1)

        treescrolly = Scrollbar(self.master, orient="vertical", command=self.tree.yview) # Scroll config
        treescrollx = Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
        treescrolly.pack(side="right", fill="y")

        self.tree["column"] = ["Name", "Value"] # Column configs
        self.tree["show"] = "headings"
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=0, width=int(self.appSizes[0]*.4),
                    stretch=NO, anchor="center") # Auto Resize

        # Database Read
        self.database = pd.read_excel(self.db)

        df_rows = self.database.to_numpy().tolist() # Database in a list of lists
        for row in df_rows:
            self.tree.insert("", "end", values=row)


        # GUI main buttons
        self.new = Button(self.master, text="New")
        self.new.pack()
        self.new.place(bordermode=OUTSIDE, relheight=.1, relwidth=.25, relx=.05, rely=.85, anchor="nw")

        self.edit = Button(self.master, text="Edit")
        self.edit.pack()
        self.edit.place(bordermode=OUTSIDE, relheight=.1, relwidth=.25, relx=.35, rely=.85, anchor="nw")


    def changeDB(self, file):
        try:
            db.createDatabase("Database", {"Filename": "TEXT"})
            db.addToDatabase("Database", "Filename", (file, ))
            print("Database local changed.")

            self.dbLabel["text"] = file
        except Exception as e:
            messagebox.showerror("ERROR", e)



def main(): # Function to initializate the app
    root = Tk() # GUI creation
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__" or True:
    print("Starting...")
    main()
