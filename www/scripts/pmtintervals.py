import time

power=30000

filedir='/Dropbox/Quanta/Data/' + time.strftime("%Y-%m-%d") + '/exppmtintervals/pmt_' + str(power) + '/'
fileprefix="counts_" + str(power)

for iii in range(200000):
    if(iii%500==0):
        self.server.speak(str(iii))
    if os.path.isfile(filedir + fileprefix + "_" + str(iii)) is True: # don't overwrite
        continue      
    if self.server.current_states['clock_working']!=15:
        self.server.speak("Pulse programmer clock not locked")
        break
    devQueue.put("PulseProgrammer;RUNPROG prog/pmtinterval.cpp")
    time.sleep(0.1)
    devQueue.put("PulseProgrammer;SPECIALREQUEST PMTREADOUT")
    time.sleep(3)
    readout=self.server.current_states['PMTREADOUT']
    if sum(row[1] for row in readout) > 1:
        f=open(filedir + fileprefix + "_" + str(iii),'w')
        f.write(str(self.server.current_states['PMTREADOUT']))
        f.close()
    if self.running != 1:
        break
