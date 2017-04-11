# chart type: 2d

self.ioXorig=self.server.current_states['CH3-0']

freq=self.server.current_states['SampFreq']

self.ioXstart= float(self.script_vars["ioXstart"])
self.ioXend= float(self.script_vars["ioXend"])
self.ioXstart2= float(self.script_vars["ioXstart2"])
self.ioXend2= float(self.script_vars["ioXend2"])
self.plotPoints= int(self.script_vars["plotPoints"])

self.ioXval=[]
self.ioXval2=[]
self.ioXval_flip=[]
self.ioX2="test"

self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)
self.ioXstep2 =  (self.ioXend2-self.ioXstart2)/(self.plotPoints-1)


for i in range(0, self.plotPoints):
    self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 6))
    self.ioXval2.append(round(self.ioXstart2+i*self.ioXstep2, 6))


self.plotInterval=(self.server.current_states["IntTime"]+50)/1000.0
self.matchvariables = 2 # device updates we need to match


for j in range(0, self.plotPoints):
    devQueue.put("FunctionGenerator;Frequency " + str(self.ioXval[j]))
    devQueue.put("PhotonCounter;SampFreq " + str(self.ioXval[j]))

    time.sleep(self.plotInterval) # put sleep before measure so there is delay for settings to take effect
    devQueue.put("FunctionGenerator;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j))
    devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j))
    while self.pause==1: # plot paused
        time.sleep(1)
    if self.running == 0: # plot stopped
        print "being killed!"
        devQueue.put("PhotonCounter;SampFreq " + str(freq))
        self.kill()
        break

for k in range(0, self.plotPoints):
    devQueue.put("FunctionGenerator;Frequency " + str(self.ioXval2[k]))
    devQueue.put("PhotonCounter;SampFreq " + str(self.ioXval2[k]))

    time.sleep(self.plotInterval) # put sleep before measure so there is delay for settings to take effect
    devQueue.put("FunctionGenerator;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j+k+1))
    devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-" + "0" + "-" + str(j+k+1))
    while self.pause==1: # plot paused
        time.sleep(1)
    if self.running == 0: # plot stopped
        print "being killed!"
        devQueue.put("PhotonCounter;SampFreq " + str(freq))
        self.kill()
        break        

devQueue.put("PhotonCounter;SampFreq " + str(freq))
    
