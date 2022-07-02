import os
import sys
import subprocess

def get_choice(prompt, choices):
    valid = False
    while not valid:
        answer = input(prompt).strip()
        valid = answer in choices
    return answer

def root_checker():
    if os.geteuid() == 0:
        print("We're root!")
    else:
        print("We're not root.")
        subprocess.call(['sudo', 'python3', *sys.argv])
        sys.exit()

def main():
    print ("hello world")

    # hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    # print(hostname)
    # hostname = input("What do you want the hostname to be?")
    # subprocess.run(["hostnamectl", "set-hostname", hostname ])
    # hostname = (subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    # print(hostname)


    answer = True

    returncode = subprocess.call(["/usr/bin/sudo", "/usr/bin/id"])
    subprocess.run(["ssh-keygen", "-A"])

    get_choice("Enter R to restart or Q to quit and move on to the next script",["R","Q"])


    # while answer:
    #     print("If you changed the hostname it's a good idea to restart your system")
    #     user_input = input("Enter R to restart or Q to quit and move on to the next script")
    #     user_input.upper()
    #     print(user_input)
    #     if user_input ==
    #     subprocess.run(["shutdown now"], stdout=subprocess.PIPE).stdout.decode('utf-8')





if __name__ == "__main__":
    main()