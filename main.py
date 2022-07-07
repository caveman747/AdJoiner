import os
import subprocess
import getpass
import pickle
import sys
import threading
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
import psutil as psutil
import time

from crontab import CronTab


def get_choice(prompt, choices):
    valid = False
    while not valid:
        answer = input(prompt).strip()
        answer = answer.upper()
        valid = answer in choices
        if answer not in choices:
            print("That answer is not in the list of choices, please select one of the answers below")
            for x in range(len(choices)):
                print(choices[x])
    return answer

def root_checker():
    if os.geteuid() == 0:
        print("We're root!")
    else:
        print("We're not root. Enter the root password")
        sudo_password = getpass.getpass(prompt='sudo password: ')
        #below command just writes the output of ls with sudo to stderr making it "disappear"
        p = subprocess.Popen(['sudo', '-S', 'ls'], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)

        try:
            out, err = p.communicate(input=(sudo_password + '\n').encode(), timeout=5)

        except subprocess.TimeoutExpired:
            p.kill()

def ChangeHostname(hostname):


    subprocess.run(["hostnamectl", "set-hostname", hostname])

    # answer = get_choice("Would you like to change your hostname?", ["YES","NO"])
    #
    # if answer == "NO":
    #     exit()
    #
    # if answer == "YES":
    #     hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    #     print("Currently, your hostname is " + hostname)
    #     hostname = input("What do you want the hostname to be?")
    #     subprocess.run(["hostnamectl", "set-hostname", hostname])
    #     hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    #     print("Your hostname will be changed to " + hostname + " You must reboot the computer for the change to take effect")

        # reboot = get_choice("Do you want to reboot now?", ["YES", "NO"])
        # if reboot == "YES":
        #     subprocess.run(["reboot", "now"])

def main():
    # root = tk.Tk()
    #
    # canvas1 = tk.Canvas(root, width=400, height=300)
    # canvas1.pack()
    #
    # if os.geteuid() == 0:
    #     label1 = tk.Label(root, text= "We rooted!")
    #     canvas1.create_window(200,230, window=label1)
    #     root.mainloop()
    # else:
    #     label2 = tk.Label(root, text="Exiting program please restart as root")
    #     canvas1.create_window(200, 230, window=label2)
    #     root.mainloop()
    #     time.sleep(10)
    #
    #     exit()

            # getpassword = entry1.get()
            # subprocess.Popen(['sudo', '-S', 'ls'], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            #                  stdin=subprocess.PIPE)



    #button1 = tk.Button(text="Enter root password to elevate program", command=root_checker)
    #canvas1.create_window(200, 180, window=button1)



    # root = tk.Tk()
    # root.withdraw()
    # answer = askyesno('ADJoiner', 'Do you want to change hostname?')
    # #root.deiconify()
    # root.destroy()
    #
    # if answer == True:
    #     root = tk.Tk()
    #
    #     canvas1 = tk.Canvas(root, width=400, height=300)
    #     canvas1.pack()
    #
    #     entry1 = tk.Entry(root)
    #     canvas1.create_window(200, 140, window=entry1)
    #
    #     def ChangeHostname():
    #         hostname = entry1.get()
    #         subprocess.run(["hostnamectl", "set-hostname", hostname])
    #         root.destroy()
    #
    #     button1 = tk.Button(text="Enter new hostname", command=ChangeHostname)
    #     canvas1.create_window(200, 180, window=button1)
    #
    #     root.mainloop()
    #
    # root = tk.Tk()
    # root.withdraw()
    # answer = askyesno('ADJoiner', 'Reboot now for hostname change to take effect?')
    #
    # if answer == True:
    #     subprocess.run(["reboot", "now"])



    # with open("/home/john/PycharmProjects/AdJoiner/mirror", "wb") as fp:
    #    pickle.dump(sys.argv[0], fp)
    #
    users = psutil.users()

    userList = []

    for i in (users):
        userList.append(i.name)

    print(userList)


    # users = subprocess.check_output("who")
    # set([x.split()[0] for x in users.splitlines()])
    # print(users)

    for i in userList:
        cron = CronTab(user=i)
        job = cron.new(command="/usr/bin/python3 /home/" + i +"/PycharmProjects/AdJoiner/testonboot.py")
        job.every_reboot()
        cron.write()
    #
    # with open("/home/john/PycharmProjects/AdJoiner/mirror", "rb") as fp:
    #     sys.argv[0] = pickle.load(fp)
    # exit()

https://stackoverflow.com/questions/72633558/cant-make-a-cron-python-script-which-uses-tkinter


if __name__ == "__main__":
    main()