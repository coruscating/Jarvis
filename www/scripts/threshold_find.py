# takes threshold data automatically
# counts 

from subprocess import call
import datetime
import random

# time in seconds for pulse programmer script to run
scriptruntime=5
strikes=0
ionthreshold=8000 # ion-less threshold
ddscon_ionthreshold=1000
startlifetime=1000
progdir="/Dropbox/Quanta/Software/GitHub/DeviceWorkers/prog/"
filename='/Dropbox/Quanta/Automated data/2015-07-30/ion_lifetime.log'
trials=2

starttime=time.time()
startcounts=self.server.current_states['Count']

while self.running==1:

    if startcounts <= ionthreshold:
        execfile("../www/scripts/load_ion.py")
        time.sleep(1)
    
    devQueue.put("PulseProgrammer;RUNPROG prog/threshold_find.cpp\n")

    # wait for script to finish
    while self.server.current_states['PP_status']=="AVR":
        time.sleep(0.5)
    
    devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT\n")
    readout=self.server.current_states['READOUT']

    scriptruntime=startlifetime/1000.0*2

    startcounts=self.server.current_states['Count']
    if startcounts <= ionthreshold:
        continue
    self.server.speak("Lifetime %d" %(startlifetime))
    # regular expressions to change turn off time
    call(["sed", "-i", "0,/OFFTIME.*/s/OFFTIME.*/OFFTIME " + str(startlifetime) + "/", progdir + "dark_lifetime.cpp"])
    devQueue.put("PulseProgrammer;RUNPROG prog/dark_lifetime.cpp\n")
    time.sleep(scriptruntime)

    print "counts=%d" %(self.server.current_states['Count'])
    while True:
        devQueue.put("PulseProgrammer;SPECIALREQUEST READOUT\n")
        time.sleep(1)
        readout=self.server.current_states['READOUT']
        if readout[trials][1]!=0 or (readout[1][1] <= ddscon_ionthreshold):
            break
    if self.server.current_states['Count'] <= ionthreshold: # ion lost
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
        startlifetime=1000+1000*random.randint(0,4)
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
        startlifetime=2000+1000*random.randint(0,5)
        

'''
def tune_lasers():
    pass
    
    cur1092DAC=self.server.current_states['DAC0offset']
    cur1092freq=self.server.current_states['WaveMeterChannel3']
    for i in range(0,10):
        cur1092DAC=cur1092DAC-0.002
        devQueue.put("LaserController;DAC0offset " + cur1092DAC)
        
    '''

