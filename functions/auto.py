# Libs Import
from bs4 import BeautifulSoup as BS
import requests
import numpy as np

# Function to web scrapt data from some sources
def getData(source, dataName):  # Ex.: source -> coinmarketcap; dataName -> bitcoin
    try:
        if source == "coinmarketcap":
            # Using the https://github.com/TulioHRC/GetCryptoPrices as reference
            page = requests.get(f"https://coinmarketcap.com/pt-br/currencies/{dataName}/")

            soup = BS(page.text, "html.parser")

            if soup.find(class_="priceValue smallerPrice").find("span"):
                return str(soup.find(class_="priceValue smallerPrice").find("span").string.strip())[2:]

    except Exception as e:
        print(f"An error has occured!\n{e}\n")
        return False


def sourcesList():   # Returns the list of websites that are compatible to the app
    return ["coinmarketcap"]


def autoLoad(database, source):   # Run the auto mode and save new data in the database 
    # database = xls file readed; source = xls file local;
    try:
        dbList = database.to_numpy().tolist()
        db = database.copy()

        changes = 0 # Number of changes made, to avoid not usefull processing

        for row in dbList:
            if row[-1] == row[-1]: # NaN returns false
                db.loc[dbList.index(row), "Value"] = getData(row[-1].split("-")[0], row[-1].split("-")[1])
                if row[-1] != db.loc[dbList.index(row), "Value"]:  # Change made
                    changes += 1

        if changes:
            db.to_excel(source, index=False) # Save Changes

        return db
    except Exception as e:
        print(e)
    