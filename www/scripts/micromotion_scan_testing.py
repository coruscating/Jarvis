# scan micromotion horizontally
# increase side while decreasing mids and ends




'''
    Define IO's you will be using
'''

#Electrodes
ElectrodeS1 = ['Q27','Q28','Q29']
ElectrodeS2 = ['Q63','Q64','Q65']



'''
    Get starting values
'''
Side1_init = {}
Side2_init = {}

for e in ElectrodeS1:
    Side1_init[e] = float(self.server.current_state[e])

for e in ElectrodeS2:
    Side2_init[e] = float(self.server.current_state[e])


'''
Define scan paramaters, Start point, end point, number of points.
'''
self.ioXstart=0
self.ioXend=0.2
self.ioYstart=0
self.ioYend=0.2
self.plotPoints=20
self.plotPoints2=20
self.ioXval=[]
self.ioXval2=[]
self.ioYval=[]

 

self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)
self.ioXstep2 = (self.ioXend-self.ioXstart)/(self.plotPoints-1)
self.ioYstep = (self.ioYend-self.ioYstart)/(self.plotPoints2-1)

for i in range(0, self.plotPoints):
    self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 3))

for j in range(0, self.plotPoints2):
    self.ioYval.append(round(self.ioYstart+j*self.ioYstep, 3))


self.ioXval2=self.ioXval

self.ioXval=[x+self.ioXorig for x in self.ioXval]
self.ioXval2=[x+self.ioXorig2 for x in self.ioXval2]
self.ioYval=[x+self.ioYorig for x in self.ioYval]

print self.ioXval
print self.ioXval2
print self.ioYval

self.plotInterval=0.5
self.ioX = "Q27"
self.ioY = "Q63"



for i in range(0, self.plotPoints):
    for e in ElectrodeS1:
        devQueue.put(e+" " + str(self.ioXval[i]) + "\n")
    for e in ElectrodeS2:
        devQueue.put(e+" " + str(self.ioXval[i]) + "\n")    

    for j in range(0, self.plotPoints2):
        time.sleep(self.plotInterval/2)
        devQueue.put("TrapElectrodes;ZoneSetSide 28" + " " + str(self.ioYval[j]))
        time.sleep(self.plotInterval/2) # put sleep before measure so there is delay for settings to take effect
        devQueue.put("PhotonCounter;
        PLOTSCRIPTHEAT" + self.timeID + "-" + str(i) + "-" + str(j))
        while self.pause==1: # plot paused
            time.sleep(1)
        if self.running == 0: # plot stopped
            self.kill()
            break
    if self.running == 0:
        break
        

