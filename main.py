import os
import subprocess
import getpass
import pickle
import sys
from crontab import CronTab
import tkinter as tk



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

def ChangeHostname():

    answer = get_choice("Would you like to change your hostname?", ["YES","NO"])

    if answer == "NO":
        exit()

    if answer == "YES":
        hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        print("Currently, your hostname is " + hostname)
        hostname = input("What do you want the hostname to be?")
        subprocess.run(["hostnamectl", "set-hostname", hostname])
        hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        print("Your hostname will be changed to " + hostname + " You must reboot the computer for the change to take effect")

        # reboot = get_choice("Do you want to reboot now?", ["YES", "NO"])
        # if reboot == "YES":
        #     subprocess.run(["reboot", "now"])


def main():
    window = tk.Tk()

    label = tk.Label(text="If you wish to change the hostname, enter it below")
    entry = tk.Entry()
    label.pack()
    entry.pack()
    hostname = entry.get()

    with open ("test.txt","wb")



    window.mainloop()

    # with open("/home/john/PycharmProjects/AdJoiner/mirror", "wb") as fp:
    #    pickle.dump(sys.argv[0], fp)
    #
    # from crontab import CronTab
    # cron = CronTab(user=True)
    # job = cron.new(command="/usr/bin/python3 /home/john/PycharmProjects/ADJoiner/testoasdfsnboot.py")
    # job.every_reboot()
    # cron.write()
    #
    # with open("/home/john/PycharmProjects/AdJoiner/mirror", "rb") as fp:
    #     sys.argv[0] = pickle.load(fp)
    # exit()




if __name__ == "__main__":
    main()