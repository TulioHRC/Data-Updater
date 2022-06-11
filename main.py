import pandas as pd
from tkinter import *
from tkinter import messagebox
from functions import files as f
from functions import database as db


class MainApp: # Main class
    def __init__(self, master):
        self.master = master
        self.master.title("Data Updater")
        self.master.geometry("400x400+100+100")

        # Database filename
        try:
            self.db = db.getDatabase("Database")
        except: # Create database of filename
            db.createDatabase("Database", {"Filename": "TEXT"})
            db.addToDatabase("Database", "Filename", ("./database.xls", ))

        self.db = db.getDatabase("Database")["Filename"].values[0]

        # Database selector
        self.dbLabel = Label(self.master, text=self.db)
        self.dbLabel.grid(row=2, column=2)
        self.dbDefiner = Button(self.master, text="Change DB", command=lambda: f.fileSelect([("Excel files", ".xls")], self.changeDB))
        self.dbDefiner.grid(row=1, column=2)

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
