#pragma once

#include "DDScon.h"
#include "HELPERS.h"

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    int plotindex=0;
    uint32_t freq=0;
    int loops=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    
    uint32_t freq_p12_p52 = MHz(118.812);
    uint32_t freq_sideband= MHz(0.284);
    uint32_t freq_n12_p32 = MHz(120.256);
    
    uint32_t Pi_time = us(10);
    uint32_t Repump_time = us(20);
    uint32_t Pi_polar = us(8);
    
    int scloopsO;
    int scloopsI;

    
	Clear_mem(d);


    red.SetAmp(51000);
    red.Update();
    
    int Nloops= 200;
    uint32_t det_time=us(1000);
    uint32_t red_time= us(10);
    uint32_t start = MHz(118.811);
    uint32_t end = MHz(119.0);
    uint32_t step = kHz(10);
    
    uint32_t recool_time=us(1000);
    uint32_t repump_time=us(20);
    
    for( freq = start;freq <= end;freq = freq + step){
        a = 0;
        d.Timing.WaitForTime(ms(5));

        for( loops=0;loops<Nloops;loops++) {            
            //Turn off doppler
            blue.Disable();
            ir1092.Disable();
            
            //Pulse 674 and count
            pmtcounts=RedPulseDetect(d, red,ir1092,blue,freq,red_time, det_time);
            
            if (pmtcounts <= 8){
               a+=1;
               }
            else{
               a+=0;
               // enable 1033
               d.Pmt0.Clear();
               ir1033.Set(1);
               d.Timing.WaitForTime(repump_time);
               pmtcounts = d.Pmt0.GetCount();
               if(pmtcounts <=8){
                //No ion! break loop
                loops = Nloops;
               }
               else{
               // still Ions! recool
               d.Timing.WaitForTime(recool_time);
               }
            }
            
          
        }
        d.Plot.SetPoint(plotindex,a);
        plotindex++;
    }
    red.Disable();
  
}



