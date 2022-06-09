from tkinter import filedialog, messagebox

def fileSelect(filetypes="", nextFunction=""): # Just select a file
    try:
        file = filedialog.askopenfilename(filetypes=filetypes)

        if not (nextFunction):
            return file
        else:
            nextFunction(file) # If given
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
        print(e)
