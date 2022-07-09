import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, askquestion, showinfo


class AskChangeHostname(tk.Tk):
    def __init__(self, title, geometry):
        super().__init__()

        # configure the root window
        AskChangeHostname.title = self.title(title)
        AskChangeHostname.geometry = self.geometry(geometry)

        # label
        self.label = ttk.Label(self, text='Do you want to change hostname?')
        self.label.pack()

    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to quit?')
        return answer

        # button


if __name__ == "__main__":
    app = AskChangeHostname()
    app.mainloop()