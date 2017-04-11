# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from Peak_detect import detect_peaks
import scipy as sp
import scipy.optimize as optimize
import ast
from scipy import special
from scipy import misc
from scipy.optimize import curve_fit
import operator
from scipy.optimize import curve_fit


programdirectory = "/Dropbox/Quanta/Software/GitHub/DeviceWorkers/prog/"
helpersdirectory = "/Dropbox/Quanta/Software/GitHub/DeviceWorkers/ddslib/"
vars=['loops', 'peak', 'width', 'stepsize'];



def Om_genrabi(Om_rabi,eta_LD,n,s):
    '''
        returns the generalized rabi frequency Omega_{n,n+s}
        Om_rabi: on-resonance carrier rabi-frequency
        eta_LD: lambda dicke parameter = np.sqrt( hbar/(2*m*Om_sec) )
        n: starting motional stateob
        s: change in motional state, e.g. s = -1, driving on the -1 sideband.
    '''

    
    FactorialRatio = 1 / np.sqrt((reduce(operator.mul,range(n,n+abs(s),1),1)))


    return Om_rabi*np.exp(-eta_LD**2/2.0)*eta_LD**(abs(s))*FactorialRatio*(special.eval_genlaguerre(n,abs(s),eta_LD**2))


def Rabi_oscil(t,Om_rabi,nbar,eta_LD,thres_Offset):
    '''
        Rabi oscillation with many motional states
    '''
    c_n = []
    for i in range(0,100):
        c_n.append((thermal_dist(i,nbar))*(np.cos(Om_genrabi(Om_rabi,eta_LD,i,0)*t/2.0)) )

    return 0.5*(1 - sum(np.array(c_n)))+thres_Offset


def thermal_dist(n,nbar):
    return (1/(nbar+1))*(nbar / (nbar +1 ))**n


def scan_fit_function(data_array):
    x = data_array[:,0]
    y = data_array[:,1]
    plt.scatter(x,y/500.0)

    fitfunc = lambda p,x : Rabi_oscil(x,p[0],p[1],p[2],p[3])
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function

    p_guess=[np.pi*2/13.5,20,1.05239636e-01,0.05]
    popt,pcov = curve_fit(Rabi_oscil,x,y/500.0,p0=p_guess)
    print 'popt= ',popt

    x1 = np.arange(0,100,.25)

    yplot = fitfunc(popt,x1)
    plt.plot(x1,yplot, label = str('RabiFreq= '+ str(round(popt[0],3)) + '\n' + 'ThermalDistAvg = '+ str(round(popt[1],3)) + '\n' + 'LambDicke= '+ str(round(popt[2],3)) + '\n' + 'Offset= ' + str(round(popt[3],3))))
    plt.legend()
    plt.xlim(0,100)
    plt.ylim([0,1])
    plt.show()

def peak_fit_function(data_array):
    x = dataarray[:,0]
    y = dataarray[:,1]

    peak_frequencies = detect_peaks(y,mph = 40, mpd = 100)
    xindex = []new_freq_peak
    for i in peak_frequencies:
        xindex.append(i)



    fitfunc = lambda p, x: p[0]+p[1]*(p[2]**2/((x-p[3])**2+p[2]**2)) # Lorentzian target
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function

    maximumfreqs = []
    for i in range(len(xindex)):
        background = 0
        A = float(y[xindex[i]])
        width = 20
        Cav0 = float(x[xindex[i]])
        p0 = [background, A, width, Cav0]
        resolution = 500
        if xindex[i] == xindex[0]:
            start = 0
            if len(xindex)!=1:
                end = (float(x[xindex[i]])+float(x[xindex[i+1]]))/2
            elif len(xindex) == 1:
                end = x[-1]
        elif xindex[i] == xindex[-1]:
            start= (float(x[xindex[i]])+ float(x[xindex[i-1]]))/2
            end = x[-1]
        else:
            start = (float(x[xindex[i]])+ float(x[xindex[i-1]]))/2
            end = (float(x[xindex[i]])+float(x[xindex[i+1]]))/2
        xfit=x[start:end]
        yfit=y[start:end]

        p1, success = optimize.leastsq(errfunc, p0[:], args=(xfit, yfit))
        yplot=fitfunc(p1,x)
        maximumfreqs.append([x[sp.argmax(yplot)],yplot[sp.argmax(yplot)]])

    freqarray = np.asarray(maximumfreqs)
    xfreq = freqarray[:,0]
    yfreq = freqarray[:,1]
    new_freq_peak =  xfreq[sp.argmax(yfreq)]

    #  for line in file(datadirectory+file_name):
    #      if "peak" in line:
    #          freqname = line.split('stepsize')[0].split('peak":"')[1].split('","')[0]
    #          break


    # call(["sed", "-i", "0,/freqname.*/s/freqname.*/freqname " + str(new_freq_peak) + "/", helpersdirectory + "HELPERS.h"])




for f in vars:
    if f not in self.script_vars.keys():
        self.server.speak("variables incomplete: %s not found") %(str(f))
        sys.exit()
    exec(f + "='" + self.script_vars[f] + "'") # assign variable

loops=int(loops)
width=float(width)
stepsize=float(stepsize)

# set parameters in script to the values we want
call(["sed", "-i", "0,/peak.*/s/peak.*/peak " + str(peak) + "/", programdirectory + "reddetect_thres.cpp"])
call(["sed", "-i", "0,/loops.*/s/loops.*/loops " + str(loops) + "/", programdirectory + "reddetect_thres.cpp"])
call(["sed", "-i", "0,/width.*/s/width.*/width kHz(" + str(width) +')' + "/", programdirectory + "reddetect_thres.cpp"])
call(["sed", "-i", "0,/stepsize.*/s/stepsize.*/stepsize kHz(" + str(stepsize) +')' + "/", programdirectory + "reddetect_thres.cpp"])


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

devQueue.put("PulseProgrammer;RUNPROG prog/redoscillation.cpp\n")

# calculate how long the script runs for approximately
sleeptime=0.002*loops*2*width/stepsize+10

for i in range(0,20):
    time.sleep(sleeptime/20)
    # readout, need ID so that ScriptReceivedData() knows which window to plot in
    devQueue.put("PulseProgrammer;SPECIALREQUESTSCRIPT" + self.timeID + " READOUT")
    if self.running==0:
        sys.exit()
