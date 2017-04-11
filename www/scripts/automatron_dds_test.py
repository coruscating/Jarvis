# Takes doppler scan, peak spectroscopy, and branching ratio data for different B fields
from __future__ import division
from subprocess import call
import datetime
import random
import time
import os.path


# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionscriptthreshold=2500
ionthreshold=5000 # ion-less threshold
iongoodthreshold=6000 # want ion above this threshold to make sure frequencies in right place

cycles=1000000

ircenterfreq=274.58905
bluecenterfreq=355.48128
irlowfreq=ircenterfreq-0.00008
irhighfreq=ircenterfreq+0.00008
bluelowfreq=bluecenterfreq-0.00005
bluehighfreq=bluecenterfreq+0.00005
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/ddslib/"
filedir='/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") + '/'

starttime=time.time()

currents=[2,2.5,3,3.5,4,4.5]
filename="test.cpp"

#self.server.speak("branching ray sho automatron online")
for iii in range(1,600000):
            #power=45000-(detuning-205)*500
            fileprefix="10x10uspulses_fixedtime2"

            while self.running==1:
                if os.path.isfile(filedir + "ddstest_" + fileprefix + "_" + str(iii)) is True: # don't overwrite
                    break
                else:
                    self.server.speak("data set %d " %(iii))
                    devQueue.put("PulseProgrammer;RUNPROG prog/" + filename)
                    time.sleep(1)
                    devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
                    time.sleep(10)
                    readout=self.server.current_states['PMTREADOUT']
                    f=open(filedir + "ddstest_" + fileprefix + "_" + str(iii),'w')
                    f.write(str(self.server.current_states) + '\n' + str(readout))
                    f.close()
