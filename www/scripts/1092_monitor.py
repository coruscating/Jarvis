# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
import datetime


filename='/Dropbox/Quanta/Data/2015-10-26/422_noise_eater_on.log'
print "hi"

while self.running==1:
	try:
	    f=open(filename, 'a')
	    starttime=time.time()
	    adc=self.server.current_states['Voltage'][1]
	    print adc
	    f.write("%s;%s\n"%(datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S'),adc))
	    time.sleep(1)
	    f.close()
	except Exception as e:
		print "error: %s" %(str(e))

    
