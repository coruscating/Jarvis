# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
programdirectory = "/Dropbox/Quanta/Software/GitHub/DeviceWorkers/prog/"
filename = "stateinitialization.cpp"
helpersdirectory = "/Dropbox/Quanta/Software/GitHub/DeviceWorkers/ddslib/"
vars=['loops', 'transition', 'width', 'stepsize', 'pump_transition'];

for f in vars:
    if f not in self.script_vars.keys():
        self.server.stransition("variables incomplete: %s not found") %(str(f))
        sys.exit()
    exec(f + "='" + self.script_vars[f] + "'") # assign variable

loops=int(loops)
width=float(width)
stepsize=float(stepsize)

# set parameters in script to the values we want
call(["sed", "-i", "0,/transition.*/s/transition.*/transition " + str(transition) + "/", programdirectory + filename])
call(["sed", "-i", "0,/loops.*/s/loops.*/loops " + str(loops) + "/", programdirectory + filename])
call(["sed", "-i", "0,/width.*/s/width.*/width kHz(" + str(width) +')' + "/", programdirectory + filename])
call(["sed", "-i", "0,/stepsize.*/s/stepsize.*/stepsize kHz(" + str(stepsize) +')' + "/", programdirectory + filename])
call(["sed", "-i", "0,/pump_transition.*/s/pump_transition.*/pump_transition " + str(pump_transition) + "/", programdirectory + filename])


f = file(helpersdirectory + 'HELPERS.h')
for line in f:
    if transition in line:
        freqtransition = float(line.split('(')[1].split(')')[0])
        break

# calculate the frequency for the first point of the graph
offset = freqtransition - width/1000

# set offset and stepsize for the Jarvis graph
webQueue.put("SCRIPTVAR;" + self.timeID + ";offset;" + str(offset) + '\n')
webQueue.put("SCRIPTVAR;" + self.timeID + ";stepsize;" + str(stepsize/1000) + '\n')

if self.running==0:
    sys.exit()

devQueue.put("PulseProgrammer;RUNPROG prog/stateinitialization.cpp\n")

# calculate how long the script runs for approximately
sleeptime=0.002*loops*2*width/stepsize+10

for i in range(0,20):
    time.sleep(sleeptime/20)
    # readout, need ID so that ScriptReceivedData() knows which window to plot in
    devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
    if self.running==0:
        sys.exit()
