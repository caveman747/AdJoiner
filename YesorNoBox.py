import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, askquestion



class App(tk."Tk):
    def __init__(self):
        super().__init__()


        self.confirm()

    def confirm(self):
        answer = askyesno(title="ADJoiner",
                          message="Change hostname?")
        if answer:
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()