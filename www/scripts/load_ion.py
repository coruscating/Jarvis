# loads ion automatically

import sys
import datetime

# Count is PMT box, pmt_data is pulse programmer
# pmtfactor should be 1 with pulse programmer (integration time 100 ms), 10 with PMT box (integration normalized to 1s)

# PMT settings
#pmtvar="Count"
#pmtfactor=10
# pulse programmer settings
pmtvar="pmt_data"
pmtfactor=1

vars=['freq422orig','freq422final','freq1092orig','power422orig','power422final', "freq422detuning", "power422offset", "threshold", "threshold2", "ovenpower","timeout"]

for f in vars:
    if f not in self.script_vars.keys():
        print f
        self.server.speak("variables incomplete")
        sys.exit()
    exec(f + "=" + str(self.script_vars[f])) # assign variable

ircenterfreq=274.58903
bluecenterfreq=355.48128
irlowfreq=ircenterfreq-0.00008
irhighfreq=ircenterfreq+0.00008
bluelowfreq=bluecenterfreq-0.00005
bluehighfreq=bluecenterfreq+0.00005
reset=True

# if photon counter is off, exit now...I've run the script with photon counter off too many times
if self.server.current_states[pmtvar]==0:
    self.server.speak("Photon counter off")
    sys.exit()

freq1092=self.server.current_states['WaveMeterChannel3']
if freq1092 < irlowfreq or freq1092 > irhighfreq:
    self.server.speak("1092 frequency wrong")
    sys.exit()
freq422=self.server.current_states['WaveMeterChannel6']
if freq422 < bluelowfreq or freq422 > bluehighfreq:
    self.server.speak("422 frequency wrong")
    sys.exit()


# turn on oven and set it to high first
devQueue.put("AgilentBOUSB;OvenState ON\n")
devQueue.put("AgilentBOUSB;OvenCurrentLim 2.5\n")

# get background counts at original place
devQueue.put("Shutters;Shutter405 CLOSE\n")
devQueue.put("Shutters;Shutter461 CLOSE\n")
devQueue.put("PulseProgrammer;STOPPROG\n") # stop any running programs
devQueue.put("PulseProgrammer;PARAM 0 1 0\n") # turn on 422
devQueue.put("PulseProgrammer;PARAM 1 1 2\n") # turn on 1092
devQueue.put("PulseProgrammer;PARAM 2 1 0\n") # turn off 674
devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig) + "\n")
devQueue.put("PulseProgrammer;PARAM 2 0 " + str(freq1092orig) + "\n")
devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig) + "\n")
time.sleep(0.5)
bkgcounts2=self.server.current_states[pmtvar]

# detune 422
devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig-freq422detuning) + "\n")
devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig + power422offset) + "\n")

# turn 1092 to high
#devQueue.put("PulseProgrammer;PARAM 2 0 200\n")
devQueue.put("PulseProgrammer;PARAM 2 2 65535\n")

devQueue.put("Shutters;Shutter405 OPEN\n")
devQueue.put("Shutters;Shutter461 OPEN\n")
time.sleep(0.5)

bkgnum=0.0
bkgcounts=0.0

bkgcounts+=self.server.current_states[pmtvar]
bkgnum+=1.0
# wait for oven resistance to get to >= 0.5 ohm, which is when trapping happens
time.sleep(1)
#self.server.speak("warming oven")
while self.server.current_states['OvenVoltageOP']/self.server.current_states['OvenCurrentOP'] <= 0.515:
    time.sleep(0.5)
    bkgcounts+=self.server.current_states[pmtvar]
    bkgnum+=1.0
    if self.running == 0: # stopping, put things back to before
        devQueue.put("AgilentBOUSB;OvenState OFF")
        devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig) + "\n")
        devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig))
        sys.exit()
    
# don't need such a high current after oven is hot
devQueue.put("AgilentBOUSB;OvenCurrentLim " + str(ovenpower))

# set oven to more reasonable current
self.server.speak("looking for ions")

starttime=time.time() # record how long it takes to trap

falses=0

if self.running == 1: # haven't been killed yet
    # open PI shutters
    devQueue.put("Shutters;Shutter405 OPEN\n")
    devQueue.put("Shutters;Shutter461 OPEN\n")
    bkgcounts=bkgcounts/bkgnum
    
    print "background counts=%d" %(bkgcounts)
    print "background counts at final settings=%d" %(bkgcounts2)
    print "threshold=%f" %(bkgcounts+threshold)
    print "final threshold=%f" %(bkgcounts2+threshold2)
    
    # waits for counts to get high
    while 1:
        freq1092=self.server.current_states['WaveMeterChannel3']
        if freq1092 < irlowfreq or freq1092 > irhighfreq:
            self.server.speak("1092 frequency wrong")
            self.running=0
            break
        freq422=self.server.current_states['WaveMeterChannel6']
        if freq422 < bluelowfreq or freq422 > bluehighfreq:
            self.server.speak("422 frequency wrong")
            self.running=0
            break

        if self.server.current_states[pmtvar] > max(bkgcounts+threshold,200*pmtfactor):
            devQueue.put("Shutters;Shutter405 CLOSE\n")
            devQueue.put("Shutters;Shutter461 CLOSE\n")
            # put frequency back to halfway up peak
            for i in range(int(freq422detuning)):
                devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig-freq422detuning+i+1) +  "\n")
                devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig+power422offset-power422offset/freq422detuning*(i+1)) +  "\n")
                time.sleep(0.1)
                if self.server.current_states[pmtvar] <= max(bkgcounts+threshold,200*pmtfactor):
                    falses +=1
                    devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig-freq422detuning) +  "\n")
                    devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig+power422offset) +  "\n")
                    break
                time.sleep(0.3)
            devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422final) + "\n")
            devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422final) + "\n")
            if self.server.current_states[pmtvar] > max(bkgcounts2+threshold2,200): # ion trapped
                devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422final) + "\n")
                devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422final) + "\n")
                time.sleep(4) # make sure ion stays for at least 1 sec
                if self.server.current_states[pmtvar] > max(bkgcounts2+threshold2,200*pmtfactor):
                    devQueue.put("AgilentBOUSB;OvenState OFF")

                    # record loading
                    f=open('/Dropbox/Quanta/Data/Logs/load_ion.log', 'a')
                    f.write('%s;%f;%d;%d;%f;%f\n' %(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), round(time.time()-starttime, 3), self.server.current_states[pmtvar], falses, self.server.current_states['WaveMeterChannel6'], self.server.current_states['WaveMeterChannel3']))
                    f.close()
                                        
                    self.server.speak("ion trapped")
                    reset=False
                    break
                else:
                    devQueue.put("Shutters;Shutter405 OPEN\n")
                    devQueue.put("Shutters;Shutter461 OPEN\n")
                    devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig-freq422detuning) + "\n")
                    devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig+power422offset) + "\n")
            else: # no ion, try again
                devQueue.put("Shutters;Shutter405 OPEN\n")
                devQueue.put("Shutters;Shutter461 OPEN\n")
                devQueue.put("PulseProgrammer;PARAM 0 0 " + str(freq422orig-freq422detuning) + "\n")
                devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig+power422offset) + "\n")
        #bkgcounts+=self.server.current_states[pmtvar] # update background
        #bkgcounts=bkgcounts/2 
        time.sleep(0.5)
        
           
        if (time.time()-starttime > timeout) or (self.running == 0): # stopped by user or not loaded after five minutes, auto quit
            break


    if reset:
        devQueue.put("AgilentBOUSB;OvenState OFF\n")
        devQueue.put("PulseProgrammer;PARAM 0 0 0\n")
        devQueue.put("PulseProgrammer;PARAM 0 2 " + str(power422orig) + "\n")
        devQueue.put("PulseProgrammer;PARAM 2 0 0\n")
        devQueue.put("Shutters;Shutter405 CLOSE\n")
        devQueue.put("Shutters;Shutter461 CLOSE\n")

        # record stopping
        f=open('/Dropbox/Quanta/Data/Logs/load_ion.log', 'a')
        f.write('%s;%f;%d;%d;S;%f;%f\n' %(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), round(time.time()-starttime, 3), self.server.current_states[pmtvar], falses, self.server.current_states['WaveMeterChannel6'], self.server.current_states['WaveMeterChannel3']))
        f.close()
        self.kill()

