# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
programdirectory = "/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
filename = "SidebandCooling.cpp"
helpersdirectory = "/Dropbox/Quanta/Software/GitHub/ddscon/ddslib/"
vars=['loops', 'peak', 'width', 'stepsize', 'sidebandloops','initfreq'];

for f in vars:
    if f not in self.script_vars.keys():
        self.server.speak("variables incomplete: %s not found") %(str(f))
        sys.exit()
    exec(f + "='" + self.script_vars[f] + "'") # assign variable

loops=int(loops)
width=float(width)
stepsize=float(stepsize)

# set parameters in script to the values we want
call(["sed", "-i", "0,/peak.*/s/peak.*/peak " + str(peak) + "/", programdirectory + filename])
call(["sed", "-i", "0,/loops.*/s/loops.*/loops " + str(loops) + "/", programdirectory + filename])
call(["sed", "-i", "0,/width.*/s/width.*/width kHz(" + str(width) +')' + "/", programdirectory + filename])
call(["sed", "-i", "0,/stepsize.*/s/stepsize.*/stepsize kHz(" + str(stepsize) +')' + "/", programdirectory + filename])
call(["sed", "-i", "0,/sidebandloops.*/s/sidebandloops.*/sidebandloops " + str(sidebandloops) + "/", programdirectory + filename])
call(["sed", "-i", "0,/initfreq.*/s/initfreq.*/initfreq " + str(initfreq) + "/", programdirectory + filename])


f = file(helpersdirectory + 'HELPERS.h')
for line in f:
    if peak in line:
        freqpeak = float(line.split('(')[1].split(')')[0])
        break

# calculate the frequency for the first point of the graph
offset = freqpeak - width/1000

# set offset and stepsize for the Jarvis graph
webQueue.put("SCRIPTVAR;" + self.timeID + ";offset;" + str(offset) + '\n')
webQueue.put("SCRIPTVAR;" + self.timeID + ";stepsize;" + str(stepsize/1000) + '\n')

if self.running==0:
    sys.exit()

devQueue.put("PulseProgrammer;RUNPROG prog/SidebandCooling_detect.cpp\n")

while True:
    # readout, need ID so that ScriptReceivedData() knows which window to plot in
    devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
    time.sleep(2)
    if self.server.current_states['PP_status']=="MAN": # script exited
        devQueue.put("PulseProgrammer;RUNPROG prog/Reset.cpp\n")
        sys.exit()
    if self.running==0:
        devQueue.put("PulseProgrammer;STOPPROG") 
        sys.exit()