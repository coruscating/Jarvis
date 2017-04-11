ScriptPlotType="none";    
ScriptVars["freq422orig"]=200;
ScriptVars["power422orig"]=43000;
ScriptVars["freq1092orig"]=200;
ScriptVars["freq422final"]=205;
ScriptVars["power422final"]=43000;
ScriptVars["freq422detuning"]=10; //detuning in ddscon units (2 MHz)
ScriptVars["power422offset"]=5000;
ScriptVars["threshold"]=2000; // threshold for ion detection
ScriptVars["threshold2"]=3000; // threshold after moving back up peak
ScriptVars["timeout"]=250;
ScriptVars["ovenpower"]=1.8;


ScriptText="load ion script will try to load at freq422orig-freq422detuning and power422orig+power422offset, and end up at freq422final, power422final.";


