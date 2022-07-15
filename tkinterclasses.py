import main
from main import *
import subprocess

import tkinter as tk

#the skeleton of this is ripped directly from the answer to this stack overflow question
#https://stackoverflow.com/questions/63017238/how-to-switch-between-different-tkinter-canvases-from-a-start-up-page-and-return

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._mainCanvas = None
        self.title("AdJoiner")
        # The dictionary to hold the class type to switch to
        # Each new class passed here, will only have instance or object associated with it (i.e the result of the Key)
        self._allCanvases = dict()
        # Switch (and create) the single instance of StartUpPage
        self.switch_Canvas(StartUpPage)

    def switch_Canvas(self, Canvas_class):

        # Unless the dictionary is empty, hide the current Frame (_mainCanvas is a frame)
        if self._mainCanvas:
            self._mainCanvas.pack_forget()

        # is the Class type passed one we have seen before?
        canvas = self._allCanvases.get(Canvas_class, False)

        # if Canvas_class is a new class type, canvas is False
        if not canvas:
            # Instantiate the new class
            canvas = Canvas_class(self)
            # Store it's type in the dictionary
            self._allCanvases[Canvas_class] = canvas

            # Pack the canvas or self._mainCanvas (these are all frames)
        canvas.pack(pady=60)
        # and make it the 'default' or current one.
        self._mainCanvas = canvas


class StartUpPage(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        tk.Frame(self)  # Here the parent of the frame is the self instance of type tk.Canvas
        tk.Label(self, text="Welcome to AdJoiner").grid(column=0, row=0)
        tk.Label(self, text="To get started it's recommended that you change the hostname of your computer to your domains naming convention\n"
                            "For example the serial number of the computer or the name of the user using the computer")
        tk.Button(self, text="Change Hostname (Recommended)",
                  command=lambda: master.switch_Canvas(ChangeHostname)).grid(column=0, row=1)
        tk.Button(self, text="Go Straight to Downloading SSL Certificates",
                  command=lambda: master.switch_Canvas(DownloadCertificates)).grid(column=0, row=2)


class ChangeHostname(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg='blue', width=430)
        tk.Label(self, text="Change Hostname").pack(side="top", fill="x", pady=5)
        hostnameField = tk.Entry(self)
        hostnameField.pack()

        def ChangeHostname():
            hostname = hostnameField.get()
            subprocess.run(["hostnamectl", "set-hostname", hostname])


        tk.Button(self, text="Change Hostname",
                  command=lambda: [master.switch_Canvas(StartUpPage), ChangeHostname()]).pack()

        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


class DownloadCertificates(tk.Frame):  # Sub-lcassing tk.Frame
    def __init__(self, master, *args, **kwargs):
        # self is now an istance of tk.Frame
        tk.Frame.__init__(self, master, *args, **kwargs)
        # make a new Canvas whose parent is self.
        self.canvas = tk.Canvas(self, bg='yellow', width=430)
        self.label = tk.Label(self, text= "Enter the location of the SSL certificates can be IP address or pre-downloaded into a directory location").pack(side="top", fill="x", pady=5)
        self.button = tk.Button(self, text="Download Certificates from IP address",
                                command=lambda: master.switch_Canvas(StartUpPage))




        self.button.pack()
        # pack the canvas inside the self (frame).
        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)