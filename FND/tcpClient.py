import os
import socket
import sys
from datetime import datetime

path = "/mdfsvc/FND" # os.getcwd() <- doesn't work with crontab

def Main(argv):
    f = open("{}/log/clientLog_{}.txt".format(path, argv[1]), "w")

    TCP_IP = '49.247.7.123'
    TCP_PORT = 5005
    BUFFER_SIZE = 186

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.settimeout(5)

    MESSAGE = "Thread " + argv[1]
    s.send(MESSAGE)
    while 1:
        data = s.recv(BUFFER_SIZE)
        print("{}: {}".format(MESSAGE, data))
        print(len(data))
        f.write("{} > {}: {}\n".format(datetime.now(), MESSAGE, data))
        if data == "Finished":
            print("Done!")
            break

    f.close()
    s.close()

if __name__ == "__main__":
    Main(sys.argv)
