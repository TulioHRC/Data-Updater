import sqlite3 as sql
import pandas as pd

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

def addToDatabase(dataframe, file, newData): # Adding to the main DataBase
    # newData is in the according format (column1, column2, ...)
    print(dataframe)
    print(file)

def getDatabase(name):
    con = sql.connect(f"./data/data.sqlite")
    cur = con.cursor()

    df = pd.read_sql_query(f"SELECT * FROM {name}", con)

    con.close()

    return df

#def removeFromDatabase(name, pos): # Remove row from database
