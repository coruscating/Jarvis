# takes ion lifetime data automatically
# loads ion, runs pulse programmer script, saves number of successful trials with laser frequencies
# reloads ion when lost
# re-scans 1092 and 422 frequencies once every 30 minutes

from subprocess import call
import datetime
import random

# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionthreshold=20000 # ion-less threshold
iongoodthreshold=50000 # want ion above this threshold to make sure frequencies in right place
ddscon_ionthreshold=1000
minlifetime=1000
lifetimesteps=500
irlowfreq=274.58959
irhighfreq=274.58969
progdir="/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
filename='/Dropbox/Quanta/Data/2015-10-09/ion_lifetime_900_baseline.log'
trials=2
exit_flag=False

starttime=time.time()
startcounts=self.server.current_states['Count']
startlifetime=minlifetime

while self.running==1:

    freq1092=self.server.current_states['WaveMeterChannel3']
    if freq1092 < irlowfreq or freq1092 > irhighfreq:
        self.server.speak("1092 not locked")
        sys.exit()

    if startcounts <= ionthreshold:
        execfile("../www/scripts/load_ion.py")
        time.sleep(1)
        
    scriptruntime=startlifetime/1000.0*2

    startcounts=self.server.current_states['Count']
    if startcounts <= ionthreshold:
        continue
    # if counts aren't above good threshold then we need to adjust 1092
    if startcounts <= iongoodthreshold:
        self.server.speak("Counts too low")
        sys.exit()
    self.server.speak("Lifetime %d" %(startlifetime))
    # regular expressions to change turn off time
    call(["sed", "-i", "0,/OFFTIME.*/s/OFFTIME.*/OFFTIME " + str(startlifetime) + "/", progdir + "DarkLifetime.cpp"])
    devQueue.put("PulseProgrammer;RUNPROG prog/DarkLifetime.cpp\n")
    time.sleep(scriptruntime)
    
    while self.server.current_states['PP_status']=="AVR":
        time.sleep(1)

    print "counts=%d" %(self.server.current_states['Count'])

    devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT\n")
    time.sleep(1)
    readout=self.server.current_states['READOUT']

    if self.server.current_states['Count'] <= ionthreshold: # ion lost
        freq1092=self.server.current_states['WaveMeterChannel3']
        if freq1092 < irlowfreq or freq1092 > irhighfreq:
            self.server.speak("1092 not locked")
            sys.exit()
        losttrial=trials
        for l in range(len(readout)):
            if readout[l][1] <= ddscon_ionthreshold:
                print "read lost ion at %d, counts=%d" %(l, readout[l][1])
                self.server.speak("lost ion, reloading")
                losttrial=l-1
                break
    
        # logfile format: timestamp, ion start counts, shutoff time, number of successes, 422 freq, 1092 freq
        f=open(filename, 'a')
        f.write('%s;%s;%d;%d;%d;%f;%f;%s\n' %(datetime.datetime.fromtimestamp(starttime), datetime.datetime.fromtimestamp(time.time()), startcounts, startlifetime, losttrial, self.server.current_states['WaveMeterChannel6'], self.server.current_states['WaveMeterChannel3'], str(readout[0:trials+1])))
        f.close()
        # random walk around where we are
        startlifetime=minlifetime+lifetimesteps*random.randint(0,3)
        #startlifetime=startlifetime+400*random.randint(-1,2)
        #if startlifetime >= 6400:
        #    startlifetime = 6400
        starttime=time.time()
        continue

        # while loop will auto reload ion
    else:
        f=open(filename, 'a')
        f.write('%s;%s;%d;%d;%d;%f;%f;%s\n' %(datetime.datetime.fromtimestamp(starttime), datetime.datetime.fromtimestamp(time.time()), startcounts, startlifetime, trials, self.server.current_states['WaveMeterChannel6'], self.server.current_states['WaveMeterChannel3'], str(readout[0:trials+1])))
        f.close()
        # random lifetime so we don't introduce bias into data
        startlifetime=minlifetime+lifetimesteps*random.randint(0,3)
 

'''
def tune_lasers():
    pass
    
    cur1092DAC=self.server.current_states['DAC0offset']
    cur1092freq=self.server.current_states['WaveMeterChannel3']
    for i in range(0,10):
        cur1092DAC=cur1092DAC-0.002
        devQueue.put("LaserController;DAC0offset " + cur1092DAC)
        
    '''

