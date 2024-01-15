import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk
from functions import files as f
from functions import database as db
from functions import auto


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
            db.addToSQLDatabase("Database", "Filename", ("./database.xls", ))

        try: # if file not found
            self.db = db.getDatabase("Database")["Filename"].values[0]
            self.database = pd.read_excel(self.db)
            
        except:
            db.deleteDatabaseFile()
            self.restart()

        # Database selector
        self.dbLabel = Label(self.master, text=self.db)
        self.dbLabel.pack()
        self.dbLabel.place(bordermode=OUTSIDE, relheight=.05, relwidth=.3, relx=.65, rely=.8, anchor="nw")

        self.dbDefiner = Button(self.master, text="Change DB", command=lambda: f.fileSelect([("Excel files Old", ".xls"), ("Excel files", ".xlsx")], self.changeDB))
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
        
        # Database read
        self.database = auto.autoLoad(self.database, self.db) # Auto reloads the values that are in auto mode

        df_rows = self.database.to_numpy().tolist() # Database in a list of lists
        for row in df_rows:
            self.tree.insert("", "end", values=row)

        # GUI main buttons
        self.new = Button(self.master, text="New", command=self.Frame)
        self.new.pack()
        self.new.place(bordermode=OUTSIDE, relheight=.1, relwidth=.25, relx=.05, rely=.85, anchor="nw")

        self.edit = Button(self.master, text="Edit", command=lambda: self.Frame(edit=self.tree.item(self.tree.focus())))
        self.edit.pack()
        self.edit.place(bordermode=OUTSIDE, relheight=.1, relwidth=.25, relx=.35, rely=.85, anchor="nw")


    def changeDB(self, file):
        try:
            if file == "": return False
            db.createDatabase("Database", {"Filename": "TEXT"})
            db.addToSQLDatabase("Database", "Filename", (file, ))
            print("Database local changed.")

            self.dbLabel["text"] = file
            self.restart()
        except Exception as e:
            messagebox.showerror("ERROR", e)

    def restart(self):
        self.master.destroy()
        main()

    class AutoSetup:
        def __init__(self, changeAuto):
            self.w = Toplevel()
            self.w.title("Auto mode Setup")
            self.w.grab_set()
            self.w.geometry(f"{int(app.appSizes[0]*.4)}x{int(app.appSizes[1]*.4)}+{app.appSizes[2]}+{app.appSizes[3]}")

            # Select between the compatibility websites (coinmarketcap)
            self.source = StringVar()
            self.sourceMenu = OptionMenu(self.w, self.source, *auto.sourcesList())
            self.sourceMenu.pack()
            self.sourceMenu.place(bordermode=OUTSIDE, relheight=.2, relwidth=.8, relx=.1, rely=.05)
            # Object name Entry
            self.nameL = Label(self.w, text="Object Name")
            self.nameL.pack()
            self.nameL.place(bordermode=OUTSIDE, relheight=.2, relwidth=.8, relx=.1, rely=.25)
            self.name = Entry(self.w)
            self.name.pack()
            self.name.place(bordermode=OUTSIDE, relheight=.2, relwidth=.8, relx=.1, rely=.45)

            self.confirm = Button(self.w, text="Apply", command=lambda: self.testApply(self.source.get(), self.name.get(), changeAuto))
            self.confirm.pack()
            self.confirm.place(bordermode=OUTSIDE, relheight=.2, relwidth=.4, relx=.3, rely=.7)

        def testApply(self, source, name, changeFunc):
            if auto.getData(source, name): # If it exists
                changeFunc(f"{source};{name}")
                messagebox.showinfo("Auto mode saved")
                self.w.destroy()
            else:
                messagebox.showerror("Error", "Nothing can be finded in the filters you selected.")



    class Frame: # Edit and New Frame - Inherit Object
        def __init__(self, edit=0):
            self.screen = Toplevel()
            title = "Edit Data" if edit else "New Data"
            self.screen.title(f"{title}") #if edit else "New Data"}")
            self.screen.grab_set() # Defines main window
            self.screen.geometry(f"{int(app.appSizes[0]*.6)}x{int(app.appSizes[1]*.6)}+{app.appSizes[2]}+{app.appSizes[3]}")

            self.nameLabel = Label(self.screen, text="Name")
            self.nameLabel.pack()
            self.nameLabel.place(bordermode=OUTSIDE, relheight=.15, relwidth=.35, relx=.1, rely=.05)
            self.nameEntry = Entry(self.screen)
            self.nameEntry.pack()
            self.nameEntry.place(bordermode=OUTSIDE, relheight=.15, relwidth=.35, relx=.55, rely=.05)

            self.valueLabel = Label(self.screen, text="Value")
            self.valueLabel.pack()
            self.valueLabel.place(bordermode=OUTSIDE, relheight=.15, relwidth=.35, relx=.1, rely=.3)
            self.valueEntry = Entry(self.screen)
            self.valueEntry.pack()
            self.valueEntry.place(bordermode=OUTSIDE, relheight=.15, relwidth=.35, relx=.55, rely=.3)

            self.autoMode = Button(self.screen, text="Auto Mode", command=lambda: app.AutoSetup(self.changeAuto))
            self.autoMode.pack()
            self.autoMode.place(bordermode=OUTSIDE, relheight=.15, relwidth=.8, relx=.1, rely=.55)

            self.auto = "" # "Source-Name"

            if not edit:
                self.createButton = Button(self.screen, text=title,
                                command=lambda: db.addToDatabase(app.database, app.db, pd.DataFrame(data={
                                    "Name": [self.nameEntry.get()],
                                    "Value": [self.valueEntry.get()],
                                    "Auto": [self.auto]
                                }), app.restart))
                # app.database it's the excel dataframe,and the app.db is the filename of the excel
                self.createButton.pack()
                self.createButton.place(bordermode=OUTSIDE, relheight=.15, relwidth=.8, relx=.1, rely=.8)
            else:
                try:
                    self.nameEntry.delete(0, END)
                    self.nameEntry.insert(0, edit["values"][0])

                    self.valueEntry.delete(0, END)
                    self.valueEntry.insert(0, edit["values"][1])

                    self.auto = edit["values"][2]

                    self.editButton = Button(self.screen, text=title,
                                    command=lambda: db.editDatabase(app.database, app.db,
                                                        ["Name", edit["values"][0]],
                                                        [self.nameEntry.get(), self.valueEntry.get(), self.auto],
                                                        ["Name", "Value", "Auto"],
                                                        app.restart))
                    self.editButton.pack()
                    self.editButton.place(bordermode=OUTSIDE, relheight=.15, relwidth=.8, relx=.1, rely=.8)
                except Exception as e:
                    messagebox.showerror("ERROR", "No data is selected, so the program can't open this page.")

        def changeAuto(self, newAuto):
            self.auto = newAuto


def main(): # Function to initializate the app
    global app, root

    root = Tk() # GUI creation
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__" or True:
    print("Starting...")
    main()
