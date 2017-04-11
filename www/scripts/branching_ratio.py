# takes ion lifetime data automatically
# loads ion, runs pulse programmer script, saves number of successful trials with laser frequencies
# reloads ion when lost
# re-scans 1092 and 422 frequencies once every 30 minutes

from subprocess import call
import datetime
import random
import os.path

# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionthreshold=20000 # ion-less threshold
iongoodthreshold=50000 # want ion above this threshold to make sure frequencies in right place
ddscon_ionthreshold=1000
minlifetime=100000
lifetimesteps=500
irlowfreq=274.58960
irhighfreq=274.59967
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
filename='/Dropbox/Quanta/Data/2015-10-16/branching_ratio_measurement_48000_50000.log'
scriptname="BranchingRatio_Measurement.cpp"
trials=2
exit_flag=False

starttime=time.time()
startcounts=self.server.current_states['Count']
startlifetime=minlifetime


# write the header
if os.path.isfile(filename) != True:
    f=open(filename, 'a')
    f.write("# Ion start time;experiment start time;starting params;ending params;number of loops;data;PMT data\n")
else: 
    f=open(filename, 'a')

while self.running==1:

    freq1092=self.server.current_states['WaveMeterChannel3']
    if freq1092 < irlowfreq or freq1092 > irhighfreq:
        self.server.speak("1092 not locked")
        sys.exit()

    if startcounts <= ionthreshold:
        execfile("../www/scripts/load_ion.py")
        time.sleep(1)

    scriptruntime=startlifetime/1E6*150

    startcounts=self.server.current_states['Count']
    if startcounts <= ionthreshold:
        continue
    # if counts aren't above good threshold then we need to adjust 1092
    if startcounts <= iongoodthreshold:
        self.server.speak("Counts too low")
        sys.exit()
    startparams=self.server.current_states

    self.server.speak("Branching ratio %d" %(startlifetime))
    # regular expressions to change turn off time
    call(["sed", "-i", "0,/loops.*/s/loops.*/loops " + str(startlifetime) + "/", progdir + scriptname])
    devQueue.put("PulseProgrammer;RUNPROG prog/" + scriptname)

    time.sleep(1)

    # wait for script to finish
    while self.server.current_states['PP_status']=="AVR":
        time.sleep(1)
        if self.server.current_states['clock_working'] != 15:
            self.server.speak("clock not locked")
            f.write('clock not locked\n')
            devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp")
            sys.exit()
        
        #f.write('%s;%f;%f\n') %(time.time(),float(self.server.current_states['WaveMeterChannel3']),float(self.server.current_states['WaveMeterChannel5']))
        if self.running==0:
            devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp")
            sys.exit()

    endcount=self.server.current_states['Count']
    devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT")
    devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
    time.sleep(1)
    readout=self.server.current_states['READOUT']
    pmtreadout=self.server.current_states['PMTREADOUT']

    if self.server.current_states['Count'] <= ionthreshold: # ion lost
        freq1092=self.server.current_states['WaveMeterChannel3']
        if freq1092 < irlowfreq or freq1092 > irhighfreq:
            self.server.speak("1092 not locked")
            f.write('%s;%s;%s;%s;%d;%s;%s\n' %(datetime.datetime.fromtimestamp(starttime), datetime.datetime.fromtimestamp(time.time()), startparams, self.server.current_states, startlifetime, str(readout), str(pmtreadout)))
            f.close()
            sys.exit()
    
        # logfile format: timestamp, ion start counts, shutoff time, number of successes, 422 freq, 1092 freq
        f=open(filename, 'a')
        f.write('%s;%s;%s;%s;%d;%s;%s\n' %(datetime.datetime.fromtimestamp(starttime), datetime.datetime.fromtimestamp(time.time()), startparams, self.server.current_states, startlifetime, str(readout), str(pmtreadout)))

        # new ion, new start time
        starttime=time.time()
        # while loop will auto reload ion
        continue

        
    else: # ion not lost
        f=open(filename, 'a')
        f.write('%s;%s;%s;%s;%d;%s;%s\n' %(datetime.datetime.fromtimestamp(starttime), datetime.datetime.fromtimestamp(time.time()), str(startparams), str(self.server.current_states), startlifetime, str(readout), str(pmtreadout)))
        f.close()
        sys.exit()

'''
def tune_lasers():
    pass
    
    cur1092DAC=self.server.current_states['DAC0offset']
    cur1092freq=self.server.current_states['WaveMeterChannel3']
    for i in range(0,10):
        cur1092DAC=cur1092DAC-0.002
        devQueue.put("LaserController;DAC0offset " + cur1092DAC)
        
    '''

