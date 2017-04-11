#
# Python daq server
# July-August 2014, Helena Zhang
#
# based on the MTserver architecture
# and websocket codes from
# -https://gist.github.com/rich20bb/4190781
# -https://gist.github.com/jkp/3136208
#
# This is a threaded server using sockets and websockets:
# -main thread for user input and handing off new connections
# -one devThread for each device which listens for device data
# -one webThread for each web client which listens for requests
# -one sendwebThread total to broadcast device data to all web clients
# -one senddevThread total to send commands to specific devices
# -one plotThread for each active plot initiated by the client
# -one scriptThread for each script being run
# -one lockThread for each active lock
#
# thread-safe communication facilitated by two queues:
# self.server.webQueue containing data from devices to be sent to web clients
# self.server.devQueue containing requests from web clients to be sent to devices
#
# See README.md for more information
#

import struct
import socket
import Queue
import sys, os
import threading
import argparse
import time, datetime
import select
import traceback
import subprocess
import json # for easy reading of dictionary file
from collections import deque
from pymongo import MongoClient

from devThread import devThread
from webThread import webThread


#############################
##### Global variables ######
#############################

DICT_FILE = "devices_dict" # dictionary file with IP and port of each device server
IOMAP_FILE = "methods_dict" # dictionary file with all methods available
LOG_DIR = "/Dropbox/Quanta/Data/"

DEBUG = False # toggle to change debugging
TEST = False

#############################
###### End of globals #######
#############################



class Server:
    def __init__(self, port):
        #Get the IP address of host computer
        self.hostname = socket.gethostname()
        self.host = socket.gethostbyname(self.hostname)
        self.port = port

        self.server = None
        self.mainthreads = []
        self.devthreads = []
        self.webthreads = []
        self.plotthreads = []
        self.lockthreads = []
        self.scriptthreads = []
        self.plotdict = {}
        self.scriptdict = {}
        self.plotqueuedict = {}
        self.plot2dqueuedict = {} # unpaired updates
        self.scriptplot2dqueuedict = {} # unpaired updates
        self.lockdict = {}
        self.current_states = {} # keeps all current values from MTservers for scripts
        self.script_vars = {} # keeps script parameters
        self.speaklog = deque([str(datetime.datetime.now()) + ": websocket server started"],maxlen=20) # previously spoken things

        self.webQueue = Queue.Queue(maxsize=0)
        self.devQueue = Queue.Queue(maxsize=0)

        self.IOMap = json.load(open(IOMAP_FILE))
        
        self.threadDict = {
            'main': self.mainthreads,
            'dev': self.devthreads,
            'web': self.webthreads,
            'plot': self.plotthreads,
            'script': self.scriptthreads,
            'lock': self.lockthreads
        }

        self.devdict = {}
        self.workerName = "Server"

        # self.f = file("messageLog.txt", "w")

        self.deadThreads = []
        self.serverLock = threading.Lock()


    def openSocket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.settimeout(None)

            #self.server.bind((self.host,self.port))
            self.server.bind(("0.0.0.0",self.port))
            self.server.listen(5)

            print "Server accepting connections on %s ip:%s port: %s"%(self.hostname,self.host,str(self.port))

        except socket.error, (value,message):
            if self.server:
                self.server.close()

            print "ERROR: Could not open socket: " + message
            print traceback.format_exc()
            sys.exit(1)



    # TODO: Make sure that nothing can destroy/remove a thread while
    # a long message is being broadcast, is it OK to block the server
    # while sending? -> Probably OK, other thread will allocate memory
    # for the function call and the message won't get lost
    def broadcastMessage(self, message):
        for thread in self.webthreads:
            thread.sendMessage(message)

        threadNum = len(self.webthreads)
        self.debugMsg("Broadcasting a message to all web threads: NUM = " + str(threadNum))

    def senddevMessage(self, message):
        # sample message: Shutters;CLOSE 405
        #                 Shutters;UPDATETIME 0.1
        self.debugMsg("sending dev message %s" %(message))
        device = message.split(';')[0]
        message = message.split(';')[1]

        if TEST == False:
            try:
                self.devdict[device].sendMessage(message)
            except Exception as e:
                print "Error sending message to %s: %s" %(device, e)
                print traceback.format_exc()

    def removeClient(self, clientThread, type):
        self.serverLock.acquire()
        try:
            self.threadDict[type].remove(clientThread)
            self.deadThreads.append(clientThread)
        except Exception as e:
            print "Error when removing %s client: %s" %(type, str(e))
            print traceback.format_exc()

        self.serverLock.release()


    def addConnDev(self, deviceKey):
        k=deviceKey
        deviceIP = self.devices[k].split(':')[0]
        devicePort = self.devices[k].split(':')[1]

        try: # try to connect to each device in file
            deviceconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            deviceconn.settimeout(5); # only set timeout for connecting to device
            deviceconn.connect((deviceIP, int(devicePort)))
            deviceconn.settimeout(None);
            newdeviceThread = devThread(deviceconn, k, self)
            newdeviceThread.start()
            self.devdict[k] = newdeviceThread
            self.serverLock.acquire()
            self.devthreads.append(newdeviceThread)
            self.serverLock.release()
            print "Connected to %s" %(k)
            return True
        except Exception, e:
            print "Can't connect to %s, error %s" %(k, str(e))
            print traceback.format_exc()
            return False

    def delConnDev(self, deviceKey): # disconnect from device
        try:
            killthread=self.devdict[deviceKey]
            killthread.kill()
            killthread.join()
            return True
        except Exception as e:
            print "Error when stopping device connection: %s" %(str(e))
            print traceback.format_exc()
            return False

    def delPlot(self, plotKey): # stop plot in progress
        try:
            killthread=self.plotdict[plotKey]
            killthread.kill()
            killthread.join()
            return True
        except Exception as e:
            print "Error when deleting plot: %s" %(str(e))
            print traceback.format_exc()
            return False

    def delScript(self, scriptKey): # stop plot in progress
        try:
            print "deleting script"
            killthread=self.scriptdict[scriptKey]
            killthread.kill()
            killthread.join()
            return True
        except Exception as e:
            print "Error when stopping script thread: %s" %(str(e))
            print traceback.format_exc()
            return False

    def pausePlot(self, plotKey):
        try:
            pausethread=self.plotdict[plotKey]
            # pause if unpause and resume if paused
            if pausethread.pause==0:
                pausethread.pause=1
            else:
                pausethread.pause=0
            return True
        except Exception as e:
            print "Error when pausing plot thread: %s" %(str(e))
            print traceback.format_exc()
            return False

    def unLock(self, lockIO): # stop plot in progress
        killthread=self.lockdict[lockIO]
        try:
            killthread.kill()
            killthread.join()
            return True
        except Exception as e:
            print "Error when stopping plot thread: %s" %(str(e))
            print traceback.format_exc()
            return False

    def run(self):
      try:
        self.openSocket()

        inputSources = [self.server,sys.stdin]
        running = 1
        
        global DEBUG

        if TEST == False:
            self.devices = json.load(open(DICT_FILE)) # loading device dictionary file
            keylist=self.devices.keys()
            keylist.sort()
            for k in keylist:
                self.addConnDev(k)

        print "Launching console for " + self.workerName + "...\n"
        print "Enter HELP for a list of commands"


        serverwebThread = sendwebThread(self)
        serverwebThread.start()
        self.mainthreads.append(serverwebThread)

        serverThread = senddevThread(self)
        serverThread.start()
        self.mainthreads.append(serverThread)


        while running:
            sys.stdout.write(self.workerName + "> ")
            sys.stdout.flush()
            try:
                inputready,outputready,exceptready = select.select(inputSources,[],[])
            except KeyboardInterrupt:
                print "Type KILL to exit the program"
                continue

            for s in inputready:
                if s == self.server:

                    # clear the web queue if there are no web threads
                    if len(self.webthreads) == 0:
                        while not self.webQueue.empty:
                            self.webQueue.get()

                    client = self.server.accept()
                    clientThread = webThread(client, self)
                    print "Client connected:" + str(clientThread.address)
                    clientThread.start()

                    # Process zombie clients:
                    self.serverLock.acquire()

                    while len(self.deadThreads) > 0:
                        thread = self.deadThreads[0]
                        thread.join()
                        self.deadThreads.remove(thread)

                        print "Zombie removed"

                    self.serverLock.release()

                elif s == sys.stdin:
                    text = sys.stdin.readline().rstrip()
                    textsplit = text.split(';')

                    if textsplit[0] == "SET": # setting something
                        # SET;Shutters;OPEN 405
                        self.devQueue.put(text.replace('SET;',''))
                    elif text.upper() == 'DEBUGON':
                        DEBUG=True
                    elif text.upper() == 'DEBUGOFF':
                        DEBUG=False
                    elif textsplit[0] == 'CONNECT':
                        self.addConnDev(textsplit[1])
                    elif textsplit[0] == 'DISCONNECT':
                        self.delConnDev(textsplit[1])
                    elif text.upper() == 'RELOAD': # reload devices and methods files
                        self.IOMap = json.load(open(IOMAP_FILE))
                        self.devices = json.load(open(DICT_FILE))
                    elif text.upper() == 'HELP':
                        print "The available commands are: \n\tHELP \n\tSTATUS \n\tDEVICESTATUS \n\tKILL"
                    elif text.upper() == 'DEVICESTATUS':
                        print "Connected devices:"
                        for key, value in self.devdict.iteritems():
                            print key
                    elif text.upper() == 'STATUS':
                        print "Server running on ip: %s port: %s"%(self.host,str(self.port))
                        print "Current number of connected web clients: " + str(len(self.webthreads))
                        print "Current number of connected device clients: " + str(len(self.devthreads))
                        print "Current number of plotting threads: " + str(len(self.plotthreads))
                        if len(self.plotthreads) > 0:
                            print self.plotdict
                        print "Current number of script threads: " + str(len(self.scriptthreads))
                        if len(self.scriptthreads) > 0:
                            print self.scriptdict
                        print "Current number of lock threads: " + str(len(self.lockthreads))
                        if len(self.lockthreads) > 0:
                            print self.lockdict
                    elif text.upper() == 'KILL':
                        running = 0
                    elif text.upper() == 'KILLPLOTS':
                        self.kill(self.plotthreads)
                    elif text.upper() == 'KILLPLOT':
                        self.delPlot(textsplit[1])
                    elif text.upper() == 'KILLSCRIPTS':
                        self.kill(self.scriptthreads)
                    elif text.upper() == 'KILLSCRIPT':
                        self.delScript(textsplit[1])
                    elif text.upper() == 'KILLLOCKS':
                        self.kill(self.lockthreads)
                    elif text.upper() == 'KILLLOCK':
                        self.unLock(textsplit[1])
                    elif text.upper() == 'KILLWEBS':
                        self.kill(self.webthreads)
                    else:
                        print "Command not recognized, enter HELP to see the list of available commands."

        # Shut down all sockets
        print "Shutting down..."
        self.server.close()
        print "Server socket closed"


        self.kill(self.mainthreads + self.devthreads + self.webthreads + self.plotthreads + self.lockthreads + self.scriptthreads)
        print "all threads should be dead"
        sys.exit(0)
      except Exception as e:
        print "Exception: %s" %(str(e))
   
    def kill(self, killList):  
        # Note that you can't iterate over the thread lists themselves as they
        # change while you are deleting the threads
        killList2=killList
        for thread in killList2:
            try:
                thread.kill()
                thread.join()
            except Exception as e:
                print "Error when removing thread: %s" %(str(e))
                print traceback.format_exc()

        for thread in self.deadThreads:
            thread.join()
        

    def speak(self, msg):
        try:
            if not os.path.exists(LOG_DIR + time.strftime("%Y-%m-%d")):
                os.makedirs(LOG_DIR + time.strftime("%Y-%m-%d"))
            f=open(LOG_DIR + time.strftime("%Y-%m-%d") + "/websocketserver.log",'a')
            f.write(str(datetime.datetime.now()) + " Script: " + msg + "\n")
            f.close()
            print msg
            subprocess.call(['pico2wave', '-w=/tmp/msg.wav', msg])
            subprocess.call(['aplay', '/tmp/msg.wav'])
        except Exception as e:
                print "Error speaking %s" %(str(e))
                print traceback.format_exc()        


    # If the debug flag is set to True, print msg to stdout
    def debugMsg(self, msg):
        global DEBUG
        if DEBUG:
            print msg

#
# broadcasts device messages to all web threads
#
class sendwebThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
        self.running = 1

    def run(self):
        while self.running:
            while not self.server.webQueue.empty():
                message = self.server.webQueue.get()
                self.server.broadcastMessage(message)
    def kill(self):
        if self.running == 1:
            self.running = 0
            self.server.removeClient(self, 'main')
    def debugMsg(self, msg):
        if self.debug:
            print msg


#
# sends to devices when self.server.devQueue is not empty
# also tries to connect to a device if client requests it
#
class senddevThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
        self.running=1

    def run(self):
        while self.running:
            while not self.server.devQueue.empty():
                message = self.server.devQueue.get()
                if message is not None:
                    try:
                        self.server.senddevMessage(message)
                    except Exception as e:
                        print "Error sending to device %s" %(message)
                        print traceback.format_exc()
    def kill(self):
        if self.running == 1:
            self.running = 0
            self.server.removeClient(self, 'main')
    def debugMsg(self, msg):
        if self.debug:
            print msg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal websocket server black-boxing communication with device servers")

    parser.add_argument("-p", "--port", default=9999, type=int, help="port to run on, default 9999")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug messages")
    parser.add_argument("-t", "--test", action="store_true", help="test mode")
    parser.add_argument("-f", "--file", default="devices_dict", help="device file, default devices_dict")
    args = vars(parser.parse_args(sys.argv[1:]))

    import importlib
    if args["debug"] == True:
        DEBUG = True

    if args["test"] == True:
        print "setting TEST to true"
        TEST = True
    DICT_FILE = args["file"]

    server = Server(args["port"])
    server.run()
