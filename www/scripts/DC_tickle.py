# chart type: 2d

self.ioXorig=self.server.current_states['CH1-0']

freq=self.server.current_states['SampFreq']

self.ioXstart= float(self.script_vars["ioXstart"])
self.ioXend= float(self.script_vars["ioXend"])
self.plotPoints= int(self.script_vars["plotPoints"])

self.ioXval=[]
self.ioXval_flip=[]
self.ioX2 = "PARAM 3 1"

self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)



for i in range(0, self.plotPoints):
    self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 6))
    self.ioXval_flip.append(round(self.ioXend-i*self.ioXstep, 6))

self.ioXval2 = [0]

self.plotInterval=(self.server.current_states["IntTime"]+50)/1000.0
self.matchvariables = 2 # device updates we need to match

devQueue.put("FunctionGenerator;Amplitude 8")
devQueue.put("FunctionGenerator;Output ON")


for j in range(0, self.plotPoints):
    devQueue.put("FunctionGenerator;Frequency " + str(self.ioXval[j]))
    devQueue.put("PhotonCounter;SampFreq " + str(self.ioXval[j]))
    if j==0: # the first point sometimes starts high
        time.sleep(0.5)
    time.sleep(self.plotInterval) # put sleep before measure so there is delay for settings to take effect
    devQueue.put("FunctionGenerator;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j))
    devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j))


    while self.pause==1: # plot paused
        time.sleep(1)
    if self.running == 0: # plot stopped
        print "being killed!"
        devQueue.put("FunctionGenerator;Frequency " + str(freq))
        devQueue.put("PhotonCounter;SampFreq " + str(freq))
        self.kill()
        break
devQueue.put("FunctionGenerator;Frequency " + str(freq))
devQueue.put("PhotonCounter;SampFreq " + str(freq))
devQueue.put("FunctionGenerator;Output OFF")
