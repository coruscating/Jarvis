from __future__ import division
import ast
import numpy as np
from scipy import special
from scipy import misc
from scipy.optimize import curve_fit
import operator

#Constants!
hbar = 1.054*10**-34            #hbar SI units
c = 2.99792458*10**8            #speed of light [m/s]
m_Sr = 88*1.46*10**-27          #Strontium 88 mass [kg]
Om_sec = 2*np.pi*0.530*10**6    #Axial secular frequency [Hz]
Om_674 = 2*np.pi*444.777*10**12 #674 transition freq. Hz
Om_422 = 2*np.pi*710.96*10**12  #422 transition freq. Hz
k_674 = Om_674/c                # 674 k-vector
Gamma = 126*10**6               #S-P decay rate in [Hz]
Isat_422 = hbar*Om_422**3*Gamma / (4*np.pi*c**2)
print (Isat_422 * (10**3)/(10**4))*(2.0/3.0)

eta_LD = k_674*np.sqrt(hbar / (2*m_Sr*Om_sec))
print eta_LD

ndoppler = (Gamma/(2*Om_sec))
print ndoppler


def getData(fname,dtype="PP"):
    
    try:
        if dtype=="PP":
            with open(fname,'r') as myfile:
                data = myfile.read().replace('\n','')
        elif dtype =="BL":
            rlines=[1,]
            with open(fname,'r') as myfile:
                data = myfile.readlines()[1].replace('\n','')
        elif dtype == "RS":
            rlines=[1,]
            with open(fname,'r') as myfile:
                data = myfile.readlines()[1].replace('\n','')
        return np.array(ast.literal_eval(str(data)))
    except Exception as e:
        print 'Could not import data',e
        return 0
        


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
    

def Voigt(x,Amp,x0,sigma,gamma):
    z = ((x-x0) + 1j*gamma)/(sigma*np.sqrt(2))
    val=Amp*(special.wofz(z).real) / (sigma*np.sqrt(2*np.pi))
    norm = sigma *(gamma)
    return val*norm

def TwoLevel_sat(delta,s0,Amp,d0):
    gamma = 126/(2*np.pi)
    s = s0 / (1 + 4 *( (delta-d0) / gamma)**2)
    return Amp*(s/2) / (1+s)

'''
redfname="/home/X88/Dropbox (MIT)/Quanta/Data/2015-04-15/redscan1"

reddata1=getData(redfname,"RS")
reddataX= reddata1[1:,0]
reddataY= reddata1[1:,1]


from gplot import Plot
plt=Plot()
plt = Plot('labbook')
plt.plot(reddataX,reddataY)
plt.xlabel(r'Detuning (AOMSetting)[$MHz$]')
plt.ylabel(r'Scattering rate[Counts/s]')
plt.finalize()
plt.show() 


import Peak_detect

x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
# set minimum peak height = 0 and minimum peak distance = 20
test=Peak_detect.detect_peaks(reddataY, mph=40, mpd=25)
print test

'''
'''
bluefname="/home/X88/Dropbox (MIT)/Quanta/Data/2015-04-13/bluelinescan1"

bluedata1=getData(bluefname,"BL")
bluedataX= bluedata1[1:,0]*0.1*2
bluedataY= bluedata1[1:,1]/0.025
peak= np.argmax((bluedataY))
p_guess = [1,10000,bluedataX[peak]]#,126/(2*np.pi)]
popt,pcov = curve_fit(TwoLevel_sat,bluedataX[0:peak],bluedataY[0:peak],p0=p_guess)
print popt




wplot = np.arange(2*160,2*240,0.01)

Vplot = TwoLevel_sat(wplot,*popt)
#for i in wplot:
#    Vplot.append(TwoLevel_sat(i,*popt))


from gplot import Plot
plt=Plot()
plt = Plot('labbook')
plt.plot(wplot,Vplot,bluedataX,bluedataY)
plt.xlabel(r'Detuning (AOMSetting)[$MHz$]')
plt.ylabel(r'Scattering rate[Counts/s]')
plt.finalize()
plt.show()  
   
'''


#test fit from rabi-oscillation     
from scipy.optimize import curve_fit

data = getData("/media/Wigner-1TB/Dropbox (MIT)/Quanta/Data/2015-04-10/rabiscan2","PP")
p_guess=[np.pi*2/13.5,20,eta_LD,0.05]
popt,pcov = curve_fit(Rabi_oscil,data[:,0],data[:,1]/500.0,p0=p_guess)
print 'popt= ',popt
r_osc=[]
for i in data[:,0]:
    r_osc.append(Rabi_oscil(i,*popt))
    

from gplot import Plot
plt=Plot()
plt = Plot('labbook')
plt.plot(data[:,0],data[:,1]/500.0,data[:,0],r_osc)
plt.xlabel(r'red-time[$\mu s$]')
plt.ylabel(r'Shelving Prob $S_{1/2}[m=1/2]\rightarrow D_{5/2}[m=5/2]$')
plt.finalize()
plt.show()  



'''
#Check rabi oscillation with many motional states
tplot=np.arange(0,100,1)
RabiFreq= 2*np.pi*1/15.0
nbar=15

R_osc=[]
for i in tplot:
    print Rabi_oscil(i,RabiFreq,nbar,eta_LD)
    R_osc.append(Rabi_oscil(i,RabiFreq,nbar,eta_LD))
print R_osc
from gplot import Plot
plt=Plot()
plt = Plot('labbook')
plt.plot(tplot,R_osc)
plt.finalize()
plt.show()    
'''
'''
nplot = np.arange(4,800,1)
Om_genN=[]
Om_genN1=[]
Om_genN2=[]
Om_genN3=[]
for i in nplot:
    Om_genN.append(Om_genrabi(1,0.05,i,0))
    Om_genN1.append(Om_genrabi(1,0.05,i,1))
    Om_genN2.append(Om_genrabi(1,0.05,i,2))
    Om_genN3.append(Om_genrabi(1,0.05,i,3))

Check motional coupling strengths
from gplot import Plot
plt=Plot()
plt = Plot('labbook')
plt.plot(nplot,Om_genN,nplot,Om_genN1,nplot,Om_genN2)
plt.finalize()
plt.show()
'''



    
