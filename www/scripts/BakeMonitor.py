# script for running pulse programmer script
# scans red frequency and plots
# saves the scan and changes the axes
from subprocess import call
import sys
import time
import datetime


filename='/Dropbox/Quanta/TwinsData/2015-10-18/bake.log'

i=1
temp=[]


while self.running==1:
    f=open(filename, 'a')
    j=0
    starttime=time.time()
    pressure=self.server.current_states['SentorrPressure']
    print pressure
    f.write("%s;%s;"%(datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S'),pressure))
    print self.server.current_states['SourceMeterVolt']
    for i in [1,2,3,4,6,7,8]:
        devQueue.put("BakeSwitch;Switch %d\n"%(i))
        time.sleep(5)
        temp=self.server.current_states['SourceMeterVolt']
        print self.server.current_states['SourceMeterVolt']
        f.write("%f;"%(temp))
        if self.running==0:
            sys.exit()
    f.write("\n")
    f.close()

    
