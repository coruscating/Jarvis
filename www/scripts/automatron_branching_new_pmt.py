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
ionscriptthreshold=14336

cycles=1000000

irlowfreq=274.58959
irhighfreq=274.58968
bluelowfreq=355.48120
bluehighfreq=355.48130
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/ddslib/"
filedir='/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") + '/'

starttime=time.time()

currents=[2,2.5,3,3.5,4,4.5]
files=["BranchingRatio_Measurement_25us_Blue_Pulse.cpp"]
fileprefixs=["25uspulse_detuning_205_44000_new_pmt"]
filename=0
#self.server.speak("branching ray sho automatron online")
powerrange={}
powerrange[205]=range(42500, 52001, 4500)
powerrange[215]=range(38000, 49001, 4500)

for iii in range(1,20):
    for detuning in range(215,200,-10):
        for power in powerrange[detuning]:
            #power=45000-(detuning-205)*500
            fileprefix="detuning_" + str(detuning) + "_power_" + str(power)
            call(["sed", "-i", "0,/branching_ratio_detuning.*/s/branching_ratio_detuning.*/branching_ratio_detuning MHz(" + str(detuning) + ")/", progdir + "HELPERS.h"])
            call(["sed", "-i", "0,/A_Blue_Det.*/s/A_Blue_Det.*/A_Blue_Det " + str(power) + "/", progdir + "HELPERS.h"])


            while self.running==1:
                if os.path.isfile(filedir + "branchingratio_" + fileprefix + "_" + str(iii)) is True: # don't overwrite
                    break
                else:
                    self.server.speak("Detuning %d, power %d, data set %d " %(detuning, power, iii))
                    #self.server.speak("file %d, data set %d " %(filename, iii))

                    freq1092=self.server.current_states['WaveMeterChannel3']
                    if freq1092 < irlowfreq or freq1092 > irhighfreq:
                        self.server.speak("1092 frequency wrong")
                        sys.exit()
                    freq422=self.server.current_states['WaveMeterChannel6']
                    if freq422 < bluelowfreq or freq422 > bluehighfreq:
                        self.server.speak("422 frequency wrong")
                        sys.exit()

                    #devQueue.put("PulseProgrammer;RUNPROG prog/BranchingRatio_Measurement_Two_Blue_Pulses.cpp\n")
                    devQueue.put("PulseProgrammer;RUNPROG prog/" + files[filename])
                    time.sleep(5)
                    while self.server.current_states['PP_status']=="AVR":
                        time.sleep(2)
                        if self.server.current_states['clock_working']!=15:
                            self.server.speak("Pulse programmer clock not locked")
                            devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp\n")
                            sys.exit()
                        if self.running!=1:
                            sys.exit()
                        readout=self.server.current_states['READOUT']
                        readoutsum=[sum(i) for i in zip(*readout)]
                        print "average=%f" %(readoutsum[1]/len(readout))
                        if readoutsum[1]/len(readout)<4:
                            self.server.speak("Counts low")
                            sys.exit()
                            break
                    self.server.speak("Done")
                    devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
                    time.sleep(2)
                    readout=self.server.current_states['PMTREADOUT']
                    f=open(filedir + "branchingratio_" + fileprefix + "_" + str(iii),'w')
                    f.write(str(self.server.current_states) + '\n' + str(readout))
                    f.close()

                    break