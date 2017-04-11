#pragma once

#include "DDScon.h"
#include "/Dropbox (MIT)/Quanta/Software/GitHub/DeviceWorkers/ddslib/HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define peak F_Red_12_52
#define loops 200
#define width kHz(2000.0)
#define stepsize kHz(10.0)

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    int plotindex=0;
    uint32_t freq=0;
    int l=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    
    
	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();

    red.SetAmp(A_Red);
    red.Update();
    red.Disable();
    
    
    
    for( freq = peak - width;freq <= peak + width;freq = freq + stepsize){
        a = 0;
        DopplerCool(d, ir1092, blue);
        for( l=0;l<loops;l++) {            
            //turn off doppler      
            blue.Disable();
            ir1092.Disable();
            
            //turn on red for delay
            red.SetFreq(freq);  
            red.Update();
            red.Enable();            
            d.Timing.WaitForTime(T_Qubit_Pi);
            red.Disable();
            
            //Turn on doppler
            blue.Enable();
            ir1092.Enable();

            
            //count
            d.Pmt0.Clear();
            d.Timing.WaitForTime(T_Count);
            pmtcounts=d.Pmt0.GetCount();
            if (pmtcounts <= Count_Threshold){
               a+=1;
               }
            else{
               a+=0;
               }
            
            
            
            // enable 1033
            ir1033.Set(1);
            d.Timing.WaitForTime(T_Repump);
            ir1033.Set(0);
        }
    d.Plot.SetPoint(plotindex,a);
    plotindex++;
    }

    red.Disable();
  
}



