# title: 422 scan as function of 422 power
# chart type: 2d

if self.plotflag==False:
    # starting DDScon freq
    self.ioXorig=self.server.current_states['CH1-0']

    # starting DDScon amplitude
    self.ioXorig2=self.server.current_states['CH1-2']

    self.ioXstart=0.0
    # end offset for DAC3offset
    self.ioXend=30

    self.ioXstart2=0.0
    # end offset for DDScon amplitude
    self.ioXend2=500.0

    # number of points for DAC3offset scan
    self.plotPoints=25
    # number of points for DDScon amplitude scan
    self.plotPoints2=2


    self.ioXval=[]
    self.ioXval_flip=[] # for scanning backwards after a forwards scan so we don't have to walk DAC3offset
    self.ioXval2=[]


    self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)
    self.ioXstep2 = (self.ioXend2-self.ioXstart2)/(self.plotPoints2-1)



    for i in range(0, self.plotPoints):
        self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 3))
        self.ioXval_flip.append(round(self.ioXend-i*self.ioXstep, 3))
    for i in range(0, self.plotPoints2):
        self.ioXval2.append(round(self.ioXstart2+i*self.ioXstep2, 3))

    self.ioSet="PARAM 1 0"

    self.ioXval=[x+self.ioXorig for x in self.ioXval]
    self.ioXval_flip=[x+self.ioXorig for x in self.ioXval_flip]
    self.ioXval2=[x+self.ioXorig2 for x in self.ioXval2]



    self.plotInterval=0.3
    self.ioX = "PARAM 1 0"
    self.ioX2 = "PARAM 1 2"
    self.ioY = "Counts"
    self.matchvariables = 2 # device updates we need to match


    for i in range(0, self.plotPoints2):
        devQueue.put("PulseProgrammer;PARAM 1 2 " + str(self.ioXval2[i]) + "\n")
        devQueue.put("PulseProgrammer;PARAM 1 2 " + str(self.ioXval2[i]) + "\n")

        for j in range(0, self.plotPoints):
            if j != 0:
                pass
                #webQueue.put("PLOTSCRIPT2D" + self.timeID) # tell Jarvis we're starting a new series

            devQueue.put("PulseProgrammer;PARAM 1 0 " + str(self.ioXval[j]))
      
            time.sleep(self.plotInterval) # put sleep before measure so there is delay for settings to take effect
            devQueue.put("PulseProgrammer;PLOTSCRIPT2D" + self.timeID + "-" + str(i) + "-" + str(j))
            devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-" + str(i) + "-" + str(j))
            while self.pause==1: # plot paused
                time.sleep(1)
            if self.running == 0: # plot stopped
                print "being killed!"
                self.kill()
                break

        if self.running == 0:
            break
            
    # walk back to starting point
    '''
    for i in range(1, abs(int((self.ioXval[j] - self.ioXorig)*10))+1):
        if self.ioXval[j] < self.ioXorig:
            devQueue.put("LaserController;DAC3offset " + str(self.ioXval[j] + i/10))
        else:
            devQueue.put("LaserController;DAC3offset " + str(self.ioXval[j] - i/10))
        time.sleep(0.3)
    devQueue.put("LaserController;DAC3offset " + str(self.ioXorig))
    '''

else:
    print "hi"
    print message