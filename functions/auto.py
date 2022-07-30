# Libs Import
from bs4 import BeautifulSoup as BS
import requests

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


def autoLoad():   # Run the auto mode and save new data in the database
    pass ### ....