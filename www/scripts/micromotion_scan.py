# scan micromotion horizontally
# increase side while decreasing mids and ends



self.ioXorig= int(self.server.current_states['HorizComp'])
self.ioYorig= int(self.server.current_states['VertComp'])

self.ioXstart= float(self.script_vars["ioXstart"])
self.ioXend= float(self.script_vars["ioXend"])
self.ioYstart= float(self.script_vars["ioYstart"])
self.ioYend= float(self.script_vars["ioYend"])
self.plotPoints= int(self.script_vars["plotPoints"])
self.ioXval=[]
self.ioYval=[]

self.ioXstep = float(self.script_vars["ioXstep"])
self.ioYstep = float(self.script_vars["ioYstep"])

for i in range(0, self.plotPoints):
    self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 3))

for j in range(0, self.plotPoints):
    self.ioYval.append(round(self.ioYstart+j*self.ioYstep, 3))



self.ioXval=[x+self.ioXorig for x in self.ioXval]
self.ioYval=[x+self.ioYorig for x in self.ioYval]

print self.ioXval
print self.ioYval

self.plotInterval=0.5
self.ioX = "HorizComp"
self.ioY = "VertComp"



for i in range(0, self.plotPoints):
    devQueue.put("TrapElectrodesAgilent;HorizComp " + str(self.ioXval[i]) + "\n")
    for j in range(0, self.plotPoints):
        time.sleep(self.plotInterval/2)
        devQueue.put("TrapElectrodesAgilent;VertComp " + str(self.ioYval[j]))
        time.sleep(self.plotInterval/2) # put sleep before measure so there is delay for settings to take effect
        devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-" + str(i) + "-" + str(j))
        while self.pause==1: # plot paused
            time.sleep(1)
        if self.running == 0: # plot stopped
            self.kill()
            break
    if self.running == 0:
        break
