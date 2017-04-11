# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from Peak_detect import detect_peaks
import UsefulFunctions
from subprocess import call
import sys
import time
import scipy as sp
import scipy.optimize as optimize

datadirectory = "/media/Wigner-1TB/Dropbox (MIT)/Quanta/Data/"
file_name = "2015-06-16/redscan1"
#file_name = "2015-06-28/SCRIPTDDSCON1435542497.495"
helpersdirectory = "/media/Wigner-1TB/Dropbox (MIT)/Quanta/Software/GitHub/DeviceWorkers/ddslib/"

for line in reversed(open(datadirectory+file_name).readlines()):
    line = line.rstrip()
    exec("testarr=" + line[1:-1])
    dataarray = np.array(testarr)
    break

x = dataarray[:,0]
y = dataarray[:,1]
plt.plot(x,y)

peak_frequencies = detect_peaks(y,mph = 40, mpd = 100)
xindex = []
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
#    params = len(xfit)-4
 #   print params
    p1, success = optimize.leastsq(errfunc, p0[:], args=(xfit, yfit))
    yplot=fitfunc(p1,x)
    maximumfreqs.append([x[sp.argmax(yplot)],yplot[sp.argmax(yplot)]])
  #  StabCounts=fitfunc(p1,p1[3]+p1[2]) #(p1[1]-p1[0])/2+p1[0]
    #label="Maxcounts=%.2e, Cav$_0$=%.3f, \n Width=%.3f, bgcounts=%d, StabCounts=%d"%(p1[1],p1[3],p1[2],p1[0],StabCounts)
    plt.plot(x,yplot, label = str('BG= '+ str(round(p1[0],3)) + ' '+ 'Amp = '+ str(round(p1[1],3)) + ' ' + 'Width= '+ str(round(p1[2])) + ' ' + 'Center= ' + str(round(p1[3],3))))


freqarray = np.asarray(maximumfreqs)
xfreq = freqarray[:,0]
yfreq = freqarray[:,1]
new_freq_peak =  xfreq[sp.argmax(yfreq)]

print new_freq_peak

# for line in file(datadirectory+file_name):
#     if "peak" in line:
#         freqname = line.split('stepsize')[0].split('peak":"')[1].split('","')[0]
#         break


#call(["sed", "-i", "0,/freqname.*/s/freqname.*/freqname " + str(new_freq_peak) + "/", helpersdirectory + "HELPERS.h"])


plt.legend()
plt.show()
#detect_peaks(dataarray[:,1], mph=40, mpd=100, show= True)
