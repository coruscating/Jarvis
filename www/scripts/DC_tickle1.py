# chart type: 2d
import numpy as np

self.ioXorig=self.server.current_states['CH3-0']

freq=self.server.current_states['SampFreq']


self.ioXstart= freq - float(self.script_vars["Width"]/2.0)
self.ioXend= freq + float(self.script_vars["Width"]/2.0)
self.plotPoints= int(self.script_vars["plotPoints"])

self.CompStart = self.script_vars['CompStart']
self.CompEnd = self.script_vars['CompEnd']
self.StepNumber = self.script_vars['StepNumber']

self.ioXval=[]
self.ioXval_flip=[]
self.ioX2 = "PARAM 3 1"

self.ioXstep = (self.ioXend-self.ioXstart)/(self.plotPoints-1)


compensations = np.arange(self.CompStart,self.CompEnd,float((self.ComEnd - self.CompStart))/self.StepNumber)

for comps in compensations:
    devQueue.put("TrapElectrodesAgilent;HorizComp " + str(comps))
    time.sleep(.01)
    for i in range(0, self.plotPoints):
        self.ioXval.append(round(self.ioXstart+i*self.ioXstep, 6))
        self.ioXval_flip.append(round(self.ioXend-i*self.ioXstep, 6))

    self.ioXval2 = [0]

    self.plotInterval=(self.server.current_states["IntTime"]+50)/1000.0
    self.matchvariables = 2 # device updates we need to match


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
            devQueue.put("PhotonCounter;SampFreq " + str(freq))
            self.kill()
            break

    devQueue.put("PhotonCounter;SampFreq " + str(freq))
#    self.fitfunction(data_dict)
    freq=self.server.current_states['SampFreq']
    self.ioXstart= freq - float(self.script_vars["Width"]/2.0)
    self.ioXend= freq + float(self.script_vars["Width"]/2.0)


def fitfunction(self,data_dict):
    plotdataX=[]
    plotdataY=[]
    for i in datatest:
        plotdataY.append(float(i["MMAmp"]))
        plotdataX.append(float(i["Frequency"]))
    
    x=plotdataX
    y=plotdataY

    yindex=sp.argmax(y)

    # Initial guesses:
    background=0               # counts
    A=y[yindex]                     # Resonance counts
    #width=1.22373442e-01            # Width in Cav(DAC2) voltage.
    width=0.02
    Cav0=x[yindex]                  # Cavity resonance guess.
    p0 = [background, A,width, Cav0]# Initial guess for the parameters
    #p0 = [background, A, width, Cav0, 0.5]
    print p0
    # Range:
    end=yindex
    start=0
    resolution=500

    # Fit the first set
    fitfunc = lambda p, x: p[0]+p[1]*(p[2]**2/((x-p[3])**2+p[2]**2)) # Lorentzian target
    #fitfunc = lambda p, x: p[0]+p[4]*(p[1]*(p[2]**2/((x-p[3])**2+p[2]**2)))+(1-p[4])*numpy.exp(-(x-p[3])**2/p[2]**2)
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    xfit=x[start:end]
    yfit=y[start:end]
    xfit=x
    yfit=y
    params = len(xfit)-4

    if len(xfit)<3:
        print "xfit is too short!"
    p1, success = optimize.leastsq(errfunc, p0[:], args=(xfit, yfit))
    xplot=sp.linspace(x[0],x[-1],resolution)
    yplot=fitfunc(p1,xplot)
    # This is not right(?): FIXME
    StabCounts=fitfunc(p1,p1[3]+p1[2]) #(p1[1]-p1[0])/2+p1[0]
    label="Maxcounts=%.2e, Cav$_0$=%.3f, \n Width=%.3f, bgcounts=%.3f, StabCounts=%.3f"%(p1[1],p1[3],p1[2],p1[0],StabCounts)
    #label="Maxcounts=%.2e, Cav$_0$=%.3f, \n Width=%.3f, bgcounts=%d, StabCounts=%d, ratio=%f"%(p1[1],p1[3],p1[2],p1[0],StabCounts,p1[4])



        
