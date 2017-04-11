# script for measuring saturation intensity of 422 and 1092 lasers
#Works by 
# 1) Start in s state
# 2) Apply 422 laser
# 3) Measure rise and fall of p state population
# 4) Fit rise & fall to theoretical function
# 5) extract saturation intensity parameters

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import operator
from scipy import special

#Data directory and filename for testing curve fitting
datadirectory = "/Dropbox (MIT)/Quanta/Data/"
file_name = "2015-09-14/SCRIPTDDSCON1442246248.792"
file_name = "2015-10-02/branchingratio_100000"
file_name = "2015-09-24/branchingRatio_1Mrepeats"


Nloops=1000000

#Load data
for line in reversed(open(datadirectory+file_name).readlines()):
    line = line.rstrip()
    exec("testarr=" + line[1:-1])
    dataarray = np.array(testarr)
    break

x = dataarray[130:2000,0]
y = dataarray[130:2000,1]

plt.scatter(x,y)


#fitfunc = lambda p,x: p[3]*np.exp(-x/p[0])*(0.5*(1-((1 / (p[1] +1))*(p[1] / (p[1]+1))**p[2]*np.cos(x/2.0))))+p[4]
#0.5(1 - ((1 / (p[1] +1))*(p[1] / (p[1]+1))**p[2]*np.cos(x/2.0)))+p[4]
#fitfunc = lambda p,x : Rabi_oscil(x,p[0],p[1],1,p[2])
#errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    
 #t = time; s = saturation intensity; b= branching ratio p->d; 1-b = branching ratio p->s, G = p->s spontaneous emission rate 
def rise_and_decay(t, t0, s, b, G, efficiency, background1, background):
    #if t < t0:
    #    efficiency=0
    b = 1 / 13.0
    G = 0.98

    term1 = np.sqrt(1.0 + (b - 1.0) * s * (-2.0 - s + b * (4.0 + s))) 
    termexp1 = (1 + (1-b) * s - term1) * (t - t0) * G / (2 * (b - 1))
    termexp2 = (1 + (1-b) * s + term1) * (t - t0) * G / (2 * (b - 1))
    hs = 0.5 * (1.0 + np.sign(t-t0))
    bg1 = background1 * 0.5 * (1-hs)
    return 0.0 * bg1 + hs* (1.0*background + efficiency * s * (b-1.0) * (-1.0 * np.exp(termexp1) + 1.0* np.exp(termexp2))) / term1

def simple(t, t0, s, b, G, efficiency):
   # if t < t0:
    #    return 1
    #else:
    return efficiency * np.exp(-1.0 * s * b * G * (t - t0))

    #term1 = np.sqrt(1.0 + (b - 1.0) * s * (-2.0 - s + b * (.0 + s))) 
    
    #return efficiency * 2.0 * s * (b-1.0) * np.exp(-0.5 * (t - t0) * G * (s + 1 / (1.0 - b))) * np.sinh(term1 * (t - t0) * G / (2.0 * (b-1.0))) / term1


fitfunc = lambda t, p: simple(t, p[0], p[1], 0.08, 0.01, p[4])
errfunc = lambda t, p, y: fitfunc(p, t) - y# Distance to the target function
    
print x[0]

p_guess=[194,0.1, 0.1, 0.3, 5000, 1, 50]
popt,pcov = curve_fit(rise_and_decay,x,y,p0=p_guess)
print 'popt= ',popt

x1 = np.arange(x[0],x[-1],1.0)

yplotguess = rise_and_decay(x1, *p_guess)
yplot = rise_and_decay(x1, *popt)

plt.title(file_name)
plt.plot(x1,yplotguess)

plt.plot(x1,yplot)

plt.legend()
plt.xlim(x[0],x[-1])
plt.ylim([0,700])
plt.show()

