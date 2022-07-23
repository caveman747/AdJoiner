import subprocess
from bs4 import BeautifulSoup
import requests

import tkinter as tk
from tkinter.ttk import Progressbar
#the skeleton of this is ripped directly from the answer to this stack overflow question
#https://stackoverflow.com/questions/63017238/how-to-switch-between-different-tkinter-canvases-from-a-start-up-page-and-return

class AdJoiner(tk.Tk):
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
        self.canvas = tk.Canvas(self)
        tk.Label(self, text="Change Hostname").pack()
        hostnameField = tk.Entry(self)
        hostnameField.pack()

        def ChangeHostname():
            hostname = hostnameField.get()
            subprocess.run(["hostnamectl", "set-hostname", hostname])


        tk.Button(self, text="Change Hostname",
                  command=lambda: [master.switch_Canvas(StartUpPage), ChangeHostname()]).pack()

        self.canvas.pack(expand=True)


class DownloadCertificates(tk.Frame):  # Sub-lcassing tk.Frame
    def __init__(self, master, *args, **kwargs):
        # self is now an istance of tk.Frame
        tk.Frame.__init__(self, master, *args, **kwargs)
        # make a new Canvas whose parent is self.
        self.canvas = tk.Canvas(self, height=200 ,width=430)
        self.label = tk.Label(self, text= "Enter the location of the SSL certificates can be IP address or pre-downloaded into a directory location").pack(side="top", fill="x", pady=5)

        self.IPEntry = tk.Entry(self)
        self.IPEntry.pack()

        self.URL = self.IPEntry.get()


        def listContents():
            caCerts = ".crt"
            sslCerts = ".pem"
            url = self.IPEntry.get()
            page = requests.get(url).text
            soup = BeautifulSoup(page, "html.parser")
            CACertList = []
            SSLCertList = []

            for node in soup.find_all("a"):
                if node.get('href').endswith(caCerts):
                    CACertList.append(node.get("href"))

                if node.get('href').endswith(sslCerts):
                    SSLCertList.append(node.get("href"))

            header1 = "Certificate Authority Certificates:"
            header2 = "SSL Certificates:"

            CACertnames = header1 + " ".join(CACertList)
            SSLCertnames = header2 + " ".join(SSLCertList)

            output = CACertnames + "\n" + SSLCertnames

            return output


        def outputCerts():
            IPAddresOutput.config(text=listContents())

        def downloadCerts():

            url = self.IPEntry.get()

            r = requests.get(url)
            # separates elements of the returned html page into classes and therefore manipulated
            soup = BeautifulSoup(r.text, "html.parser")
            urls = []
            names = []

            # i becomes iterator to index tuples of hrefs -> urls
            for i, link in enumerate(soup.find_all("a")):
                # creates a string based off the url concats a / then the link itself for use writing to files later on
                full_URL = (url + "/" + str(link.get("href")))
                # because there will be more than just the desired hrefs (links) then this conditional below gives us just what we want
                if full_URL.endswith(".crt") or full_URL.endswith(".pem"):
                    urls.append(full_URL)
                    names.append(soup.select("a")[i].attrs["href"])

            # creates zip object tuples names and urls with an iterator for the for loop below
            names_urls = zip(names, urls)

            for name, url in names_urls:
                r = requests.get(url)
                if name.endswith(".crt"):
                    with open("/usr/share/ca-certificates/" + name, "wb") as f:
                        f.write(r.content)
                if name.endswith(".pem"):
                    with open("/etc/ssl/" + name, "wb") as f:
                        f.write(r.content)

            subprocess.run(["sudo", "update-ca-certificates"])

            output = "Certificates downloaded to the appropriate directories. Running update-ca-certificates so that certs take effect. "

            return output

        # def DownloadFinished():
        #     DownloadFinishedOutput.config(text=downloadCerts())

        self.button = tk.Button(self, text="Check IP address for certs",
                                command=lambda: outputCerts())

        self.button.pack()
        Explanation = tk.Label(self,
                               text="The contents of the IP address inputted are listed below, do you want to download all certificates found at this IP address?")
        Explanation.pack()

        IPAddresOutput = tk.Label(self)
        IPAddresOutput.pack()

        Yes = tk.Button(self, text = "Yes", command= lambda: [ master.switch_Canvas(RequiredPackagesClearCaches), downloadCerts()])
        No = tk.Button (self, text= "No", command= lambda: master.switch_Canvas(StartUpPage))

        Yes.pack()
        No.pack()

        # DownloadFinishedOutput = tk.Label(self)
        # DownloadFinishedOutput.pack()

        # pack the canvas inside the self (frame).
        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


class RequiredPackagesClearCaches(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=200 ,width=430)

        def installPackages():
            list = ["packagekit", "krb5-user", "facter", "sssd-tools", "sssd", "libnss-sss", "libpam-sss", "adcli", "samba-common-bin", "realmd", "gss-ntlmssp", "sssd-dbus", "oddjob", "oddjob-mkhomedir"]
            for i in list:
                subprocess.run(["sudo", "apt", "install", i])
                self.canvas.update_idletasks()
                pb["value"] += 7
                if i == "oddjob-mkhomedir":
                    pb["value"] = 100
                    self.canvas.update_idletasks()
                txt["text"] = pb['value'], '%'

        def clearCaches():
            subprocess.run(["systemctl", "stop", "sssd.service"])
            subprocess.run(["rm", "-rf" "/var/lib/sss/db/*"])
            subprocess.run(["rm", "/etc/krb5.keytab"])

        pb = Progressbar(self.canvas, orient=tk.HORIZONTAL, length=100, mode="determinate")
        pb.pack()

        txt = tk.Label(self.canvas, text="0", bg="#345",fg="#fff")
        txt.pack()

        StartDownload = tk.Button(self.canvas, text="Install Required Packages and clear necessary caches", command= lambda: [installPackages(), clearCaches()])
        StartDownload.pack()


        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)




