import tkinterclasses
import os
import sys



# subprocess.run(["sudo", "cp", "-i", "/home/john/PycharmProjects/AdJoiner/testonboot.py", "/bin" ])
# bridge = open("/etc/xdg/autostart/bridge.desktop", "w")
# bridge.writelines(["[Desktop Entry]", "\nType=Application", "\nName=Bridge", "\nExec=/usr/bin/python3 /bin/testonboot.py ","\nIcon=system-run", "\nX-GNOME-Autostart-enabled=true"])
# bridge.close()

def main():


    test = tkinterclasses.AdJoiner()

    test.mainloop()



if __name__ == "__main__":
    main()
