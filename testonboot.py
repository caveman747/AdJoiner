import sys
import pickle
import subprocess




with open("/home/john/PycharmProjects/AdJoiner/mirror", "rb") as fp:
    sys.argv[0] = pickle.load(fp)
subprocess.run(["sudo", "ls"])

print(test)
# subprocess.run(["ssh-keygen", "-A"])
