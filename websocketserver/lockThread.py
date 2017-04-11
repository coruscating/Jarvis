import threading
import traceback
import time
import os
import datetime
import json

#
# lockThread class
# function: handles device and Jarvis communications for locking
# sample initial request: LOCK;2352364362:DAC3offset;WaveMeterChannel6;355.481181;0.00001;0.00001;0.00001;1
#

class lockThread(threading.Thread):
    def __init__(self, server, message):
        threading.Thread.__init__(self)
        self.server = server
        self.running = 1
        self.message = message.split(";")
        timestamp, self.lockIO, self.locktoIO = self.message[1:4]
        self.lockCenter, self.lockP, self.lockI, self.lockD, self.interval, self.limits = map(float, self.message[4:])
        print self.server.current_states[self.lockIO]
        self.min=float(self.server.current_states[self.lockIO])-self.limits
        self.max=float(self.server.current_states[self.lockIO])+self.limits
        print self.min
        print self.max

        for IOdev, IOList in self.server.IOMap.iteritems():
            if self.lockIO in IOList:
                self.lockIOdev = IOdev

        # parameter we're changing is ID because that has to be unique
        self.server.lockdict[timestamp]=self

        self.Derivator=0
        self.Integrator=0

    def updateParams(self,message):
        self.message=message.split(";")
        print self.message
        self.lockCenter, self.lockP, self.lockI, self.lockD, self.interval, self.limits = map(float, self.message[4:])
        print "updated"

    def run(self):
        while self.running:
            self.updateLock()
            time.sleep(self.interval)

    def updateLock(self):
        error = self.lockCenter - float(self.server.current_states[self.locktoIO])
        P_value = self.lockP * error
        D_value = self.lockD * (error - self.Derivator)
        self.Derivator = error
        self.Integrator = self.Integrator + error
        I_value = self.Integrator * self.lockI

        PID = P_value + I_value + D_value + float(self.server.current_states[self.lockIO])

        # if exceed limits, don't do anything
        if PID > self.min and PID < self.max:
            self.server.devQueue.put(self.lockIOdev + ";" + self.lockIO + " " + str(PID) + "\n")
        else:
            print "exceeded limits, killing lock" 
            self.kill()
    def kill(self):
        if self.running == 1:
            self.running = 0
            self.server.removeClient(self, 'lock')
            
