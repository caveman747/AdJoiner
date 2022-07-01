import subprocess
from subprocess import *


def main():
    print ("hello world")

    hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print(hostname)
    hostname = input("What do you want the hostname to be?")
    subprocess.run(["hostnamectl", "set-hostname", hostname ])
    hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print(hostname)

    subprocess.run([)


if __name__ == "__main__":
    main()