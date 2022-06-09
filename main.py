import pandas as pd
from tkinter import *


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Updater")



def main(): # Função de inicialização do app
    root = Tk() # Criação do GUI
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__" or True:
    print("Starting...")
    main()
