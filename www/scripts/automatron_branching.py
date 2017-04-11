# Takes doppler scan, peak spectroscopy, and branching ratio data for different B fields

from subprocess import call
import datetime
import random
import time
import os.path

# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionscriptthreshold=2000
ionthreshold=5000 # ion-less threshold
iongoodthreshold=6000 # want ion above this threshold to make sure frequencies in right place

cycles=500000

ircenterfreq=274.58905
bluecenterfreq=355.48128
irlowfreq=ircenterfreq-0.00008
irhighfreq=ircenterfreq+0.00008
bluelowfreq=bluecenterfreq-0.00005
bluehighfreq=bluecenterfreq+0.00005
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/ddslib/"
filedir='/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") + '/'

starttime=time.time()
fileprefix="no_detuning"

currents=[2,2.5,3,3.5,4,4.5]
powerrange={}
irpowerrange=range(65000,65001,10000)
#powerrange[205]=range(42500, 52001, 4500)
powerrange=range(34000, 48001, 4000)

#self.server.speak("branching ray sho automatron online")

for iii in range(1,20):
    for irpower in irpowerrange:
        for power in powerrange:
            #power=45000-(detuning-205)*500
            fileprefix="irpower_" + str(irpower) + "_bluepower_" + str(power)
            #call(["sed", "-i", "0,/branching_ratio_detuning.*/s/branching_ratio_detuning.*/branching_ratio_detuning MHz(" + str(detuning) + ")/", progdir + "HELPERS.h"])
            call(["sed", "-i", "0,/A_Blue_Det.*/s/A_Blue_Det.*/A_Blue_Det " + str(power) + "/", progdir + "HELPERS.h"])
            call(["sed", "-i", "0,/A_1092_Det.*/s/A_1092_Det.*/A_1092_Det " + str(irpower) + "/", progdir + "HELPERS.h"])

        #for bfield in currents:
        #    devQueue.put("AgilentBOUSB;BAxialCurrentLim " + str(bfield))
        #    time.sleep(300)
        #    fileprefix="abfield_" + str(bfield) + "_no_detuning"


            while self.running==1:
                if os.path.isfile(filedir + "branchingratio_" + fileprefix + "_" + str(iii)) is True: # don't overwrite
                    break
                else:
                    self.server.speak("IR %d, blue %d, data set %d " %(irpower, power, iii))
                    startcounts=self.server.current_states['pmt_data']
                    if startcounts <= ionthreshold:
                        execfile("../www/scripts/load_ion.py")
                        self.running=1
                        time.sleep(5)

                    freq1092=self.server.current_states['WaveMeterChannel3']
                    if freq1092 < irlowfreq or freq1092 > irhighfreq:
                        self.server.speak("1092 frequency wrong")
                        sys.exit()
                    freq422=self.server.current_states['WaveMeterChannel6']
                    if freq422 < bluelowfreq or freq422 > bluehighfreq:
                        self.server.speak("422 frequency wrong")
                        sys.exit()
                    
                    startcounts=self.server.current_states['pmt_data']
                    if startcounts <= ionthreshold: # ion got lost quickly
                        strikes+=1
                        if strikes>=2:
                            self.server.speak("Too many strikes")
                            sys.exit()
                        continue
                    else:
                        strikes=0

                    #devQueue.put("PulseProgrammer;RUNPROG prog/BranchingRatio_Measurement_Two_Blue_Pulses.cpp\n")
                    devQueue.put("PulseProgrammer;RUNPROG prog/BranchingRatio_Measurement_25us_Blue_Pulse.cpp\n")
                    time.sleep(5)
                    while self.server.current_states['PP_status']=="AVR":
                        time.sleep(2)
                        if self.server.current_states['clock_working']!=15:
                            self.server.speak("Pulse programmer clock not locked")
                            devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp\n")
                            sys.exit()
                        if self.running!=1:
                            sys.exit()
                        if self.server.current_states['pmt_data']<ionscriptthreshold:
                            self.server.speak("Counts low")
                            devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp")
                            break
                    self.server.speak("Done")
                    devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
                    time.sleep(2)
                    startcounts=self.server.current_states['pmt_data']
                    if startcounts <= ionthreshold:
                        self.server.speak("Ion lost, reloading")
                        continue
                    if(self.server.current_states['read_word']!=cycles-1):
                        self.server.speak("Ion still there")
                        continue
                    time.sleep(4)
                    readout=self.server.current_states['PMTREADOUT']
                    f=open(filedir + "branchingratio_" + fileprefix + "_" + str(iii),'w')
                    f.write(str(self.server.current_states) + '\n' + str(readout))
                    f.close()
                    if startcounts <= iongoodthreshold:
                        self.server.speak("Ion counts low")
                        sys.exit()
                    break