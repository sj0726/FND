import socket
from thread import *
import threading
import datetime
import os
import time
import logging

# print_lock = threading.Lock()
BUFFER_SIZE = 186
currTime = datetime.datetime.now()
path = "/mdfsvc/FND" # os.getcwd() <- doesn't work with crontab

data = open("{}/CMEAPIOutputs.txt".format(path), "r")
lines = data.readlines()

weekday = datetime.datetime.today().isoweekday()
if weekday == 7:
    weekday = 0

log = "{}/log/serverLog_{}.txt".format(path, weekday)
logging.basicConfig(filename=log, level=logging.DEBUG, filemode='w', datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s.%(msecs)d > %(message)s')

logging.debug("Server is Starting...\n")

def threadRecv(x):
    while 1:
        data = x.recv(BUFFER_SIZE)
        if data:
            threadName = "%s" % data
        else:
            logging.debug("Done! ({})\n".format(threadName))
            # print_lock.release()
            break
        
        logging.debug("Received data (Server): {}\n".format(data))
        for l in lines:
            MESSAGE = l[:-1]
            try:
                x.send(MESSAGE)
            except:
                logging.debug("{} exited\n".format(threadName))
                break
            time.sleep(0.001)
        x.send("Finished")
    x.close()

def Main():
    TCP_IP = '49.247.7.123'
    TCP_PORT = 5005
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    logging.debug("Socket binded to: {}/{}\n".format(TCP_IP, TCP_PORT))
    s.listen(5)
    logging.debug("Socket is listening...\n")

    while 1:
        try:
            conn, addr = s.accept()
            # print_lock.acquire()
            logging.debug("Connection address: {}\n".format(addr))
            start_new_thread(threadRecv, (conn,))
        except:
            break
    
    s.close()
    logging.debug("Server Ended\n")
    log.close()

if __name__ == '__main__':
    Main()