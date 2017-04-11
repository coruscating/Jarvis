import numpy as np

x_old = 0
x_new = float(self.script_vars["HorizCompStart"])
y_old = 0
y_new = float(self.script_vars["VertCompStart"])
x_stepsize = float(self.script_vars["XStepSize"])
y_stepsize = float(self.script_vars["YStepSize"])
precision= float(self.script_vars["Precision"])
deltax = float(self.script_vars["dx"])
deltay = float(self.script_vars["dy"])
self.ioX = "HorizComp"
self.ioY = "MMAmp"
self.ioX2 = "PARAM 3 0"
self.ioXval2 = [0]

def gradMMAmp(self, x,deltax,y= None, deltay = None): #gradient of the MMAmp Function
    sleeptime = .3
    mx1 = []
    mx2 = []
##    my1 = []
##    my2 = []

    
    #calculating dx
    self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x + deltax))
    time.sleep(sleeptime)
    x2 = float(self.server.current_states['HorizComp'])
    for i in range(5):
        mx2.append(float(self.server.current_states['MMAmp']))
        time.sleep(.3)
    MMAmpx2= sum(mx2)/5.0
    self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x - deltax))
    time.sleep(sleeptime)
    x1 = float(self.server.current_states['HorizComp'])
    for i in range(5):
        mx1.append(float(self.server.current_states['MMAmp']))
        time.sleep(.3)
    MMAmpx1 = sum(mx1)/5.0
    while x2-x1 == 0:
        self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x + deltax))
        time.sleep(sleeptime)
        x2 = float(self.server.current_states['HorizComp'])
        MMAmpx2 = float(self.server.current_states['MMAmp'])
        self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x - deltax))
        time.sleep(sleeptime)
        x1 = float(self.server.current_states['HorizComp'])
        MMAmpx1 = float(self.server.current_states['MMAmp'])
    dx = (MMAmpx2 - MMAmpx1)/(x2 - x1)
    
##    #calculating dy
##    self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y + deltay))
##    time.sleep(sleeptime)
##    y2 = float(self.server.current_states['VertComp'])
##    for i in range(5):
##        my2.append(float(self.server.current_states['MMAmp']))
##        time.sleep(.3)
##    MMAmpy2 = np.mean(my2)
##    self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y - deltay))
##    time.sleep(sleeptime)
##    y1 = float(self.server.current_states['VertComp'])
##    for i in range(5):
##        my1.append(float(self.server.current_states['MMAmp']))
##        time.sleep(.3)
##    MMAmpy1 = np.mean(my1)
##    while y2 - y1 == 0:
##        self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y + deltay))
##        time.sleep(sleeptime)
##        y2 = float(self.server.current_states['VertComp'])
##        MMAmpy2 = float(self.server.current_states['MMAmp'])
##        self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y - deltay))
##        time.sleep(sleeptime)
##        y1 = float(self.server.current_states['VertComp'])
##        MMAmpy1 = float(self.server.current_states['MMAmp'])
##    dy = (MMAmpy2 - MMAmpy1)/(y2 - y1)
    
    print 'dx = ', dx

    return dx #the gradient of the MMAmp function at the indicated horiz and vert comp value


i = 0
while abs(x_new - x_old) > precision: # and abs(y_new-y_old) > precision:
    i = i + 1
    x_old = x_new
#    y_old = y_new
    gradientmmamp = gradMMAmp(self, x_old, deltax)
    x_new = x_old - x_stepsize*gradientmmamp
    print 'x_old= ', x_old, 'x_new= ', x_new
#    y_new = y_old - y_stepsize*gradientmmamp[1]
#    print 'y_old= ', y_old, 'y_new= ', y_new
#    self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y_new))
    self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x_new))
    time.sleep(.5)
##    #averaging MMAmps
##    MMAmps = []
##    for i in range(3):
##        self.server.devQueue.put("TrapElectrodesAgilent;VertComp " + str(y_new))
##        self.server.devQueue.put("TrapElectrodesAgilent;HorizComp " + str(x_new))
##        time.sleep(.5)
##        MMAmps.append(float(self.server.current_states['MMAmp']))
##    self.server.devQueue.put("PhotonCounter;MMAmp " + str(np.mean(MMAmps)))
##    time.sleep(.5)
    self.server.devQueue.put("PhotonCounter;PLOTSCRIPT2D" + self.timeID + "-0-" + str(i))
    self.server.devQueue.put("TrapElectrodesAgilent;PLOTSCRIPT2D" + self.timeID + "-0-" + str(i))
    if self.running == 0:
        self.kill()
        break


