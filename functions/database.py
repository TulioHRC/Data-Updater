import sqlite3 as sql
import pandas as pd
import os
from tkinter import messagebox

def createDatabase(name, schema): # schema format is {"column": "SQL Type"}
    con = sql.connect("./data/data.sqlite")
    cur = con.cursor()

    # Schema formatting
    table = ""
    for index, (key, value) in enumerate(schema.items()):
        table += f"{key} {value},"

    table = table[:-1]

    dropText = f"DROP TABLE IF EXISTS {name}"
    createText = f"CREATE TABLE {name} ({table})"

    cur.execute(dropText)
    cur.execute(createText) # Example of schema: {"Name": "TEXT"}

    con.close()

def addToSQLDatabase(name, schema, content): # schema format here is "column1, column2"
    con = sql.connect("./data/data.sqlite")
    cur = con.cursor()

    intergs = "?," * len(content)
    intergs = intergs[:-1]

    cur.execute(f"INSERT INTO {name} ({schema}) VALUES ({intergs})", content) # content format is (value1, value2, ...)
    con.commit()

    con.close()

def addToDatabase(dataframe, file, newData, restartFunc): # Adding to the main DataBase
    # newData is in the according format (column1, column2, ...)
    try:
        newDataframe = pd.concat([dataframe, newData], ignore_index=True)
        newDataframe.to_excel(file, index=False)

        messagebox.showinfo("Data added", "The new data was added!")

        restartFunc() # Restart app
    except Exception as e:
        messagebox.showerror("ERROR", f"Error while adding data to the database: \n{e}")

def editDatabase(dataframe, file, idInfo, newValues, columns, restartFunc):
    try:
        # idInfo is [column, value]
        newDataframe = dataframe.copy()
        newDataframe.loc[list(dataframe[idInfo[0]].values).index(idInfo[1]), columns] = newValues
        newDataframe.to_excel(file, index=False)

        messagebox.showinfo("Data Edited", "The new data was added into the database!")

        restartFunc()
    except Exception as e:
        messagebox.showerror("ERROR", f"Error while editing data in the database: /n{e}")

def getDatabase(name):
    con = sql.connect(f"./data/data.sqlite")
    cur = con.cursor()

    df = pd.read_sql_query(f"SELECT * FROM {name}", con)

    con.close()

    return df

def deleteDatabaseFile():
    os.remove("./data/data.sqlite")

#def removeFromDatabase(name, pos): # Remove row from database
