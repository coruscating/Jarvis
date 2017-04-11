# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
programdirectory = "/Dropbox/Quanta/Software/GitHub/ddscon/prog/"
vars=['loops', 'runtime', 'timestep','stateprep', 'sidebandcool', 'transition'];

for f in vars:
    if f not in self.script_vars.keys():
        self.server.speak("variables incomplete: %s not found") %(str(f))
        sys.exit()
    exec(f + "='" + self.script_vars[f] + "'") # assign variable

loops=int(loops)
runtime=float(runtime)
timestep=float(timestep)

scriptname="RamseyScan.cpp"

# set parameters in script to the values we want
call(["sed", "-i", "0,/loops.*/s/loops.*/loops " + str(loops) + "/", programdirectory + scriptname])
call(["sed", "-i", "0,/runtime.*/s/runtime.*/runtime us(" + str(runtime) +')' + "/", programdirectory + scriptname])
call(["sed", "-i", "0,/timestep.*/s/timestep.*/timestep us(" + str(timestep) +')' + "/", programdirectory + scriptname])
call(["sed", "-i", "0,/stateprep.*/s/stateprep.*/stateprep " + str(stateprep) + "/", programdirectory + scriptname])
#call(["sed", "-i", "0,/sidebandcool.*/s/sidebandcool.*/sidebandcool " + str(sidebandcool) + "/", programdirectory + scriptname])
call(["sed", "-i", "0,/qubit_transition.*/s/qubit_transition.*/qubit_transition " + str(transition) + "/", programdirectory + scriptname])




# set timestep for the Jarvis graph
webQueue.put("SCRIPTVAR;" + self.timeID + ";stepsize;" + str(timestep) + '\n')
webQueue.put("SCRIPTVAR;" + self.timeID + ";offset;" + str(0) + '\n')

if self.running==0:
    sys.exit()

devQueue.put("PulseProgrammer;RUNPROG prog/" + scriptname + "\n")

while True:
    # readout, need ID so that ScriptReceivedData() knows which window to plot in
    devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
    time.sleep(5)
    if self.server.current_states['PP_status']=="MAN": # script exited
        devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
        sys.exit()
    if self.running==0:
        sys.exit()