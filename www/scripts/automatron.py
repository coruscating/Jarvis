# Takes doppler scan, peak spectroscopy, and branching ratio data for different B fields

from subprocess import call
import datetime
import random
import time
import os.path

# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionscriptthreshold=8000
ionthreshold=20000 # ion-less threshold
iongoodthreshold=45000 # want ion above this threshold to make sure frequencies in right place
ddscon_ionthreshold=1000
minlifetime=1000
lifetimesteps=500
irlowfreq=274.58959
irhighfreq=274.58969
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
filedir='/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") + '/'

starttime=time.time()

startlifetime=minlifetime

currents=[2,2.5,3,3.5,4,4.5]


self.server.speak("automatron online")

for i in currents:
    self.server.speak("B field " + str(i))

    devQueue.put("AgilentBOUSB;BAxialCurrentLim " + str(i))
    time.sleep(300) # time for B field to adjust

    if self.running!=1:
        sys.exit()

    freq1092=self.server.current_states['WaveMeterChannel3']
    if freq1092 < irlowfreq or freq1092 > irhighfreq:
        self.server.speak("1092 frequency wrong")
        sys.exit()

    '''
    #####
    # Doppler scan
    #####

    if os.path.isfile(filedir + "dopplerscan_abfield_" + str(i)) is not True:
        while self.running==1:
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                execfile("../www/scripts/load_ion.py")
                time.sleep(5)
            
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold: # ion got lost quickly or didn't load at all
                strikes+=1
                if strikes>2:
                    self.server.speak("Too many strikes")
                    sys.exit()
                continue
            else:
                strikes=0


            self.server.speak("Taking doppler scan")
            devQueue.put("PulseProgrammer;RUNPROG prog/DopplerScan.cpp\n")
            time.sleep(5)
            while self.server.current_states['PP_status']=="AVR":
                time.sleep(1)
                if self.running!=1:
                    sys.exit()
            devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT")
            time.sleep(2)
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                self.server.speak("Ion lost, reloading")
                break
            readout=self.server.current_states['READOUT']
            f=open(filedir + "dopplerscan_abfield_" + str(i),'w')
            f.write(str(readout))
            f.close()
            break

    freq1092=self.server.current_states['WaveMeterChannel3']
    if freq1092 < irlowfreq or freq1092 > irhighfreq:
        self.server.speak("1092 frequency wrong")
        sys.exit()
    if self.server.current_states['Count']<=iongoodthreshold:
            self.server.speak("Counts low")

    #####
    # Pulsed
    #####

    if os.path.isfile(filedir + "peakspec_abfield_" + str(i)) is not True:
        while self.running==1:
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                execfile("../www/scripts/load_ion.py")
                time.sleep(5)
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold: # ion got lost quickly
                strikes+=1
                if strikes>2:
                    self.server.speak("Too many strikes")
                    sys.exit()
                continue
            else:
                strikes=0

            self.server.speak("Taking pulsed scan")
            devQueue.put("PulseProgrammer;RUNPROG prog/PulsedSpectroscopy.cpp\n")
            time.sleep(5)
            while self.server.current_states['PP_status']=="AVR":
                time.sleep(1)
                if self.running!=1:
                    sys.exit()
                if self.server.current_states['Count']<ionscriptthreshold:
                    devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp")
                    break
            devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT")
            time.sleep(2)
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                self.server.speak("Ion lost, reloading")
                continue
                
            readout=self.server.current_states['READOUT']
            f=open(filedir + "peakspec_abfield_" + str(i),'w')
            f.write(str(readout))
            f.close()
            break        

    freq1092=self.server.current_states['WaveMeterChannel3']
    if freq1092 < irlowfreq or freq1092 > irhighfreq:
        self.server.speak("1092 frequency wrong")
        sys.exit()
    if self.server.current_states['Count']<=iongoodthreshold:
            self.server.speak("Counts low")

    '''
    #####
    # Branching ratio
    #####

    if os.path.isfile(filedir + "branchingratio_abfield_" + str(i)) is not True:
        while self.running==1:
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                execfile("../www/scripts/load_ion.py")
                time.sleep(5)
            
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold: # ion got lost quickly
                strikes+=1
                if strikes>2:
                    self.server.speak("Too many strikes")
                    sys.exit()
                continue
            else:
                strikes=0

            self.server.speak("Taking branching ratio data")
            devQueue.put("PulseProgrammer;RUNPROG prog/BranchingRatio_Measurement_New.cpp\n")
            time.sleep(5)
            while self.server.current_states['PP_status']=="AVR":
                time.sleep(1)
                if self.running!=1:
                    sys.exit()
                if self.server.current_states['Count']<ionscriptthreshold:
                    devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp")
                    break
            devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
            time.sleep(2)
            startcounts=self.server.current_states['Count']
            if startcounts <= ionthreshold:
                self.server.speak("Ion lost, reloading")
                continue
            readout=self.server.current_states['PMTREADOUT']
            f=open(filedir + "branchingratio_abfield_" + str(i),'w')
            f.write(str(readout))
            f.close()          
            break