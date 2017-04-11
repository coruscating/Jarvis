import threading
import traceback
import time
import os
import datetime
import json

#
# plotThread class
# function: handles device and Jarvis communications for plotting
# sample initial request: PLOT;TIMESERIES;1409946594.606;PowerMeterPower;0.05;50
#

class plotThread(threading.Thread):
    def __init__(self, server, message):
        threading.Thread.__init__(self)
        self.server = server
        self.running = 1
        self.message = message.split(";")
        self.plottype = self.message[1]
        self.timeID = self.message[2] # Using plot start time as unique ID
        self.pause = 0
        
        self.server.plotdict[self.timeID]=self # store thread in server dictionary 
        self.dir = '/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") # folder for today's date
        
        try:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
        except Exception as e:
            print "Error when making directory: %s" %(str(e))
            print traceback.format_exc()

    def run(self):
        while self.running:
            self.plotInterval = float(self.message[3]) # in seconds
            self.plotPoints = int(self.message[4])
            
            if self.plottype == "TIMESERIES":
                self.ioName = self.message[5]
                self.ioName2 = self.message[6]
                print self.ioName2
                f=open(self.dir + '/PLOT' + self.timeID,'a')
                f.write("# Data taken beginning " + str(datetime.datetime.now()) + "\n")
                f.write("# Time series plot of %s %s with %d points with %f s time interval\n" %(self.ioName,self.ioName2,self.plotPoints,self.plotInterval))
                f.write(str(self.server.current_states))
                f.close()
                 
                for devname, iolist in self.server.IOMap.iteritems():
                    if self.ioName in iolist:
                        self.deviceName = devname
                    if self.ioName2 in iolist:
                        self.deviceName2 = devname
                if self.ioName2 == "":
                    for i in range(0, self.plotPoints):
                        self.server.devQueue.put(self.deviceName + ";PLOT" + self.timeID + "\n")          
                        time.sleep(self.plotInterval)
                        while self.pause == 1: # plot paused
                            time.sleep(1)
                        if self.running == 0: # plot stopped
                            self.kill()
                            return
                else:
                    for i in range(0, self.plotPoints):
                        self.server.devQueue.put(self.deviceName + ";PLOT" + self.timeID + "-" + str(i) + "\n")
                        if self.deviceName2 != self.deviceName:
                            self.server.devQueue.put(self.deviceName2 + ";PLOT" + self.timeID + "-" + str(i) + "\n")         
                        time.sleep(self.plotInterval)
                        while self.pause == 1: # plot paused
                            time.sleep(1)
                        if self.running == 0: # plot stopped
                            self.kill()
                            return               


                time.sleep(1) # give plot some time to finish
                self.kill()
            elif self.plottype == "2DSERIES":
                self.setVal = {}
                ioName1 = self.message[5]
                ioName2 = self.message[6]
                self.ioSet=self.message[7]
                ioStart=float(self.message[8])
                ioEnd=float(self.message[9])
                ioStep = (ioEnd-ioStart)/(self.plotPoints-1)
                ioReturn=int(self.message[10])
                
                f=open(self.dir + '/PLOT2D' + self.timeID,'a')
                f.write("# Data taken beginning " + str(datetime.datetime.now()) + "\n")
                f.write("# 2-D series plot of %s on X-axis, %s on Y-axis\n" %(ioName1,ioName2))
                f.write("# Setting %s from %f to %f, %d points with %f s time interval\n" %(self.ioSet,ioStart,ioEnd,self.plotPoints,self.plotInterval))
                f.write(str(self.server.current_states))
                f.close()
                
                # find the devices for each of the IOs
                for devname, iolist in self.server.IOMap.iteritems():
                    if ioName1 in iolist:
                        deviceName1 = devname
                    if ioName2 in iolist:                
                        deviceName2 = devname
                    if self.ioSet in iolist:
                        deviceName3 = devname
            
                for i in range(0, self.plotPoints):
                    plotid = 'PLOT2D' + self.timeID + "-" + str(i)
                    self.server.devQueue.put(deviceName3 + ";" + self.ioSet + " " + str(round(ioStart+i*ioStep, 6)) + "\n")
                    self.setVal[plotid] = round(ioStart+i*ioStep, 6)
                    time.sleep(self.plotInterval) # put sleep before measure so there is delay for settings to take effect
                    self.server.devQueue.put(deviceName1 + ";" + plotid + "\n")
                    self.server.devQueue.put(deviceName2 + ";" + plotid + "\n")
                    while self.pause==1: # plot paused
                        time.sleep(1)
                        
                    if self.running==0: # plot stopped
                        if ioReturn == 1: # return to starting value
                            self.server.devQueue.put(deviceName1 + ";" + self.ioSet + " " + str(round(ioStart, 6)) + "\n")
                        self.kill()
                        return
                time.sleep(1) # give plot some time to finish
                if ioReturn == 1: # return to starting value
                    self.server.devQueue.put(deviceName1 + ";" + self.ioSet + " " + str(round(ioStart, 6)) + "\n")
                    
                self.kill()
            elif self.plottype == "HEATMAP":
                self.plotPoints2 = int(self.message[5])
                self.ioX = self.message[6]
                self.ioY = self.message[7]
                self.ioXstart = float(self.message[8])
                self.ioXend = float(self.message[9])
                self.ioYstart = float(self.message[10])
                self.ioYend = float(self.message[11])
                self.ioMeasure = self.message[12]
                self.ioXval = []
                self.ioYval = []
                
                self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)
                self.ioYstep = (self.ioYend-self.ioYstart)/(self.plotPoints2-1)
                self.ioReturn = int(self.message[13])
                
                for i in range(0, self.plotPoints):
                    self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 6))
                for i in range(0, self.plotPoints2):
                    self.ioYval.append(round(self.ioYstart+i*self.ioYstep, 6))

                f=open(self.dir + '/PLOTHEAT' + self.timeID,'a')
                f.write("# Data taken beginning " + str(datetime.datetime.now()) + "\n")
                f.write("# Heatmap plot of %s on X-axis, %s on Y-axis\n" %(self.ioX,self.ioY))
                f.write("# X range %f to %f, Y range %f to %f\n" %(self.ioXstart, self.ioXend, self.ioYstart, self.ioYend))
                f.write("# %d X points, %d Y points with %f s time interval\n" %(self.plotPoints, self.plotPoints2, self.plotInterval))
                f.write(str(self.server.current_states))
                 
                for devname, iolist in self.server.IOMap.iteritems():
                    if self.ioX in iolist:
                        deviceName1 = devname
                    if self.ioY in iolist: 
                        deviceName2 = devname
                    if self.ioMeasure in iolist:
                        deviceName3 = devname
            
                for i in range(0, self.plotPoints):
                    self.server.devQueue.put(deviceName1 + ";" + self.ioX + " " + str(self.ioXval[i]) + "\n")
                    for j in range(0, self.plotPoints2):
                        time.sleep(self.plotInterval/2)
                        self.server.devQueue.put(deviceName2 + ";" + self.ioY + " " + str(self.ioYval[j]) + "\n")
                        time.sleep(self.plotInterval/2) # put sleep before measure so there is delay for settings to take effect
                        self.server.devQueue.put(deviceName3 + ";PLOTHEAT" + self.timeID + "-" + str(i) + "-" + str(j) + "\n")
                        while self.pause==1: # plot paused
                            time.sleep(1)
                        if self.running == 0: # plot stopped
                            if ioReturn == 1: # return to starting value
                                self.server.devQueue.put(deviceName1 + ";" + self.ioX + " " + str(round(self.ioXstart, 6)) + "\n")
                                self.server.devQueue.put(deviceName2 + ";" + self.ioY + " " + str(round(self.ioYstart, 6)) + "\n")
                            self.kill()
                            return
                time.sleep(1) # give plot some time to finish
                if self.ioReturn == 1: # return to starting value
                    self.server.devQueue.put(deviceName1 + ";" + self.ioX + " " + str(round(self.ioXstart, 6)) + "\n")
                    self.server.devQueue.put(deviceName2 + ";" + self.ioY + " " + str(round(self.ioYstart, 6)) + "\n")
                self.kill()  

    # process plot data from devices and send to Jarvis            
    def sendplot(self, id, timestamp, devname, message):  
        if id.startswith("PLOT2D"):

            try: # need to put two updates together for 2-D series
                if id in self.server.plot2dqueuedict:
                    combodict=self.server.plot2dqueuedict[id].copy()
                    combodict.update(message) # combine the two updates
                    combodict.update({self.ioSet: self.setVal[id]})
                    
                    message = id + ";" + timestamp + ";" + json.dumps(combodict)
                    
                    self.server.debugMsg("sending Jarvis " + str(message))
                    self.server.webQueue.put(message)
                    self.server.plot2dqueuedict.pop(id) # remove it from queue
                    
                    f=open(self.dir + '/PLOT2D' + self.timeID,'a')
                    f.write(message + "\n")
                    f.close()

                else:
                    # add unpaired update to queue
                    self.server.plot2dqueuedict[id] = message
            except Exception as e:
                print "Error when sending 2D plot: %s" %(str(e))
                print traceback.format_exc()
                
        elif id.startswith("PLOTHEAT"):
        # need to put three updates together for heatmap
            try:
                pointX=id.split('-')[1] # get ordinal of point
                pointY=id.split('-')[2]
                message.update({self.ioX: self.ioXval[int(pointX)],self.ioY:self.ioYval[int(pointY)]}) # add X and Y coordinate values
                message = id + ";" + timestamp + ";" + json.dumps(message)
                print "sending message" + str(message)
                self.server.webQueue.put(message)
                f=open(self.dir + '/PLOTHEAT' + self.timeID,'a')
                f.write(message + "\n")
                f.close()
            except Exception as e:
                print "Error when sending heatplot: %s" %(str(e)) 
                print traceback.format_exc()
        else:
            print id, message
            try:
                if self.ioName2 != "" and self.deviceName2 != self.deviceName:
                    if id in self.server.plotqueuedict:
                        combodict=self.server.plotqueuedict[id].copy()
                        combodict.update(message) # combine the two updates
                        
                        message = id + ";" + timestamp + ";" + json.dumps(combodict)
                        print "sending Jarvis " + str(message)
                        self.server.debugMsg("sending Jarvis " + str(message))
                        self.server.webQueue.put(message)
                        self.server.plotqueuedict.pop(id) # remove it from queue
                        f=open(self.dir + '/PLOT' + self.timeID,'a')
                        f.write(message + "\n")
                        f.close()                    

                    else:
                        # add unpaired update to queue
                        self.server.plotqueuedict[id] = message
                else:
                    message = id + ";" + timestamp + ";" + json.dumps(message)
                    print "sending Jarvis " + str(message)
                    self.server.debugMsg("sending Jarvis " + str(message))
                    self.server.webQueue.put(message)
                    f=open(self.dir + '/PLOT' + self.timeID,'a')
                    f.write(message + "\n")
                    f.close() 

            except Exception as e:
                print "Error when sending time plot: %s" %(str(e))
                print traceback.format_exc()


    def pause(self):
        if self.pause==0:
            self.pause=1
                
    def kill(self):
        if self.running == 1:
            print "setting running to 0"
            self.running = 0
            self.server.webQueue.put("PLOT" + self.timeID + ";DONE") # let Jarvis know we've stopped plotting
            self.server.removeClient(self, 'plot')


