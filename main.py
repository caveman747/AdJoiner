import tkinterclasses
import os
import sys


# subprocess.run(["sudo", "cp", "-i", "/home/john/PycharmProjects/AdJoiner/testonboot.py", "/bin" ])
# bridge = open("/etc/xdg/autostart/bridge.desktop", "w")
# bridge.writelines(["[Desktop Entry]", "\nType=Application", "\nName=Bridge", "\nExec=/usr/bin/python3 /bin/testonboot.py ","\nIcon=system-run", "\nX-GNOME-Autostart-enabled=true"])
# bridge.close()

def main():
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0')
        os.environ.__setitem__('DISPLAY', ':0')
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo..")
        args = ['pkexec', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('pkexec', *args)

    print('Running. Your euid is' + str(euid))

    test = tkinterclasses.SampleApp()

    test.mainloop()




if __name__ == "__main__":
    main()
