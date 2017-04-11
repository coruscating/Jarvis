# uses RamseyFrequencyFinder to update
from subprocess import call
import sys
import time
programdirectory = "/Dropbox/Quanta/Software/GitHub/ddscon/ddslib/"
filename = "HELPERS.h"


if self.running==0:
    sys.exit()

devQueue.put("PulseProgrammer;RUNPROG prog/Ramsey_Frequency_Finder.cpp\n")

while True:
    time.sleep(1)
# readout, need ID so that ScriptReceivedData() knows which window to plot in
    devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
    time.sleep(1)
    readout=self.server.current_states['READOUT']
    if self.running==0:
        devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp\n")
        sys.exit()
    if (readout[0][1] != 0) and (readout[3][1] != 0): 
        freq1=round((readout[0][1])/1E6,4)
        freq2=round((readout[3][1])/1E6,4)
        break

# set parameters in script to the values we want

print "New frequencies: %f MHz, %f MHz" %(freq1, freq2)



call(["sed", "-i", "0,/F_Red_n12_32.*/s/F_Red_n12_32.*/F_Red_n12_32 MHz(" + str(freq2) + ")/", programdirectory + filename])
call(["sed", "-i", "0,/F_Red_12_52.*/s/F_Red_12_52.*/F_Red_12_52 MHz(" + str(freq1) + ")/", programdirectory + filename])


# here we should check that the frequency finder is correct by doing fast ramsey scans
devQueue.put("PulseProgrammer;RUNPROG prog/RamseyScanFast.cpp\n")
time.sleep(5)
devQueue.put("PulseProgrammer;RUNPROG prog/RamseyScanFastRepump.cpp\n")
time.sleep(5)
#devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
#time.sleep(1)
#readout.self.server.current_states['READOUT']
#if 


devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp\n")
