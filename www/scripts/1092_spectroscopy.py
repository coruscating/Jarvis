# chart type: 2d

from subprocess import call
import datetime
import random
import time
import os.path

start=self.server.current_states['DAC0offset']
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
points=60
interval=0.01
val=start

devQueue.put("PulseProgrammer;RUNPROG prog/ClearMEM.cpp")

for i in range(0, points):
    val=val+interval
    print "val=" + str(val)
    devQueue.put("LaserController;DAC0offset " + str(val))
    time.sleep(0.3)
    call(["sed", "-i", "0,/plotindex.*/s/plotindex.*/plotindex " + str(i) + "/", progdir + "PulsedSpectroscopy1092.cpp"])
    devQueue.put("PulseProgrammer;RUNPROG prog/PulsedSpectroscopy1092.cpp")
    time.sleep(2)
    while self.server.current_states['PP_status']=="AVR":
        time.sleep(0.5)
    if(self.server.current_states['pmt_data']<900):
        self.server.speak("ion lost")
        sys.exit()
    while self.pause==1: # plot paused
        time.sleep(1)
    if self.running == 0: # plot stopped
        print "being killed!"
        sys.exit()
        break   
