# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
programdirectory = "/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
ionthreshold=10000

if self.plotflag==False:

    self.PlotHandlerFlag=True
    # set timestep for the Jarvis graph
    webQueue.put("SCRIPTVAR;" + self.timeID + ";stepsize;1\n")
    webQueue.put("SCRIPTVAR;" + self.timeID + ";offset;0\n")


    for i in range(0,8):
        if self.server.current_states['Count'] <= ionthreshold: # lost ion, reload
            print "lost ion, reloading"
            execfile("../www/scripts/load_ion.py")
            time.sleep(2)

        devQueue.put("PulseProgrammer;RUNPROG prog/QuantumJump.cpp\n")
        time.sleep(5) # give the ddscon time to update its status
        while self.server.current_states['PP_status']=="AVR": # script still running
            time.sleep(2)
            if self.running==0:
                sys.exit()
        self.server.speak("script %d done" %(i+1))
        devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")




else:
    f=open(self.dir + '/QUANTUMJUMP' + self.timeID,'a')
    f.write(message + "\n")
    f.close()
    self.server.webQueue.put(self.plotmessage)