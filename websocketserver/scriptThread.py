import threading
import time
import traceback
import os
import json
import ast
import sys


from StringIO import StringIO

from pymongo import MongoClient


############# MongoDB #############
client = MongoClient('quanta-rabi')
db = client.jarvis

class scriptThread(threading.Thread):
    def __init__(self, server, message):
        threading.Thread.__init__(self)
        self.server = server
        self.running = 1
        self.message = message.split(";")
        self.filename = self.message[2]
        self.timeID = self.message[1]
        self.script_vars=ast.literal_eval(self.message[3])
        self.server.scriptdict[self.timeID]=self # store thread in server dictionary 
        self.dir = '/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") # folder for today's date
        self.sendtype=0
        self.pause = 0
        self.PlotHandlerFlag=False
        self.plotflag=False
        self.filesavename='_' + self.filename.split(".")[0] + '_' + self.timeID

        try:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
        except Exception as e:
            print "Error when making directory: %s" %(str(e))
            print traceback.format_exc()
        f=open(self.dir + '/SCRIPTPLOT2D' + self.timeID,'a')
        f.write(self.filename + "\n")
        f.write(json.dumps(self.script_vars) + "\n")
        f.close()

        # mongo: insert into script { "variables": script_vars, "time": timestamp, "name": filename, "scriptid": timeID}
        db.script.insert_one(
            {"timestamp":time.time(),"variables": self.script_vars, "name":self.filename, "scriptid":self.timeID}
        )

    def run(self):
        while self.running:
            codeOut = StringIO()
            codeErr = StringIO()
            devQueue=self.server.devQueue
            webQueue=self.server.webQueue
            try:
                self.server.speak("Running script")
                execfile("../www/scripts/" + self.filename)
                self.server.speak("script stopped")
            except (SystemExit,Exception), info:
                print "Error running script: %s, %s" %(Exception, "".join([str(x) for x in info] ))
                print traceback.format_exc()
                self.server.speak("script stopped")
            print('SCRIPTSTOPPED;' + self.timeID)
            self.server.webQueue.put('SCRIPTSTOPPED;' + self.timeID)
            print(codeOut.getvalue())
            print(codeErr.getvalue())
            self.kill()
    
    def sendddsconplot(self,message):
        if self.PlotHandlerFlag==True:
            self.plotmessage=message
            self.plotflag=True
            execfile("../www/scripts/" + self.filename)
            self.plotflag=False
        else:
            self.server.webQueue.put(message)

    # process plot data from devices and send to Jarvis      
    def sendplot(self, id, timestamp, devname, message):
        self.message=message
        self.timestamp=timestamp
        #self.plotflag=True
        #execfile("../www/scripts/" + self.filename)
        #self.plotflag=False
        if id.startswith("PLOTSCRIPT2D"):
            if self.sendtype==0:
                self.server.webQueue.put(id + ";" + timestamp + ";" + '2d')
                self.sendtype=1
        
            try: # need to put two updates together for 2-D series
                        
                if id in self.server.scriptplot2dqueuedict:
                    combodict=self.server.scriptplot2dqueuedict[id].copy()
                    combodict.update(message) # combine the two updates
                    id1 = int(id.split('-')[1])
                    id2 = int(id.split('-')[2])
                    combodict.update({self.ioX2: self.ioXval2[id1]})
                    
                    message = id + ";" + timestamp + ";" + json.dumps(combodict)
                    
                    self.server.webQueue.put(message)
                    #self.server.plot2dqueuedict.pop(id) # remove it from queue
                    
                    f=open(self.dir + '/SCRIPTPLOT2D' + self.filesavename,'a')
                    f.write(message + "\n")
                    f.close()
                else:
                    # add unpaired update to queue
                    self.server.scriptplot2dqueuedict[id] = message
            except Exception as e:
                print "Error when sending 2D plot: %s" %(str(e))
                print traceback.format_exc()
                
        elif id.startswith("PLOTSCRIPTHEAT"):
        # need to put three updates together for heatmap
            try:
                pointX=id.split('-')[1] # get ordinal of point
                pointY=id.split('-')[2]
                message.update({self.ioX: self.ioXval[int(pointX)],self.ioY:self.ioYval[int(pointY)]}) # add X and Y coordinate values
                message = id + ";" + timestamp + ";" + json.dumps(message)
                print "sending message" + str(message)
                self.server.webQueue.put(message)
                f=open(self.dir + '/SCRIPTPLOTHEAT' + self.filesavename,'a')
                f.write(message + "\n")
                f.close()
            except Exception as e:
                print "Error when sending heatplot: %s" %(str(e)) 
                print traceback.format_exc()
        else:
            try:
                message = id + ";" + timestamp + ";" + devname + ";" + json.dumps(message)
                self.server.webQueue.put(message)
                f=open(self.dir + '/SCRIPTPLOT_' + self.filesavename,'a')
                f.write(message + "\n")
                f.close()
            except Exception as e:
                print "Error when sending time plot: %s" %(str(e))
                print traceback.format_exc()


                    
    def kill(self):
        if self.running == 1:
            self.running = 0
            self.server.removeClient(self, 'script')

