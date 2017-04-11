#pragma once

#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define peak F_Red_Center
#define loops 200
#define width kHz(5000.0)
#define stepsize kHz(10.0)
#define redpower 51000
#define stateprep 0
#define detecttime T_Qubit_Pi

int main()
{
    // Initialize:
    DDScon d;
    int plotindex=0;
    uint32_t freq=0;
    int l=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
    
	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();

    red.SetAmp(redpower);
    red.SetFreq(0);
    red.Update();
    red.Enable();
    
    //Initialize(d, red, ir1033, ir1092, blue, 10);
    for( freq = peak - width;freq <= peak + width;freq = freq + stepsize){
        DopplerCool(d, ir1092, blue);
        for( l=0;l<loops;l++) { 
            //turn off doppler 
            ir1033.Set(0);
            blue.SetFreq(MHz(0));
            blue.Update();
            ir1092.Disable();
            
            //state prep
            if (stateprep==1){
                Initialize(d, red, ir1033, ir1092, blue, 10);
            }

            //turn on red for delay
            red.SetFreq(freq);  
            d.Timing.ZeroTime();
            red.Update();
            //d.Timing.WaitForTime(us(100)); //for power 6000
            red.SetFreq(0);
            d.Timing.WaitUntilTime(detecttime);
            red.Update();
            
            //Turn on doppler
            blue.SetFreq(F_Blue_Det);
            blue.SetAmp(A_Blue_Det);
            blue.Update();
            ir1092.Enable();

            //count
            d.Pmt0.Clear();
            d.Timing.WaitForTime(T_Count);
            pmtcounts=d.Pmt0.GetCount();
            if (pmtcounts <= Count_Threshold){
               d.Plot[plotindex]+=1;
            }
            
            // enable 1033
            ir1033.Set(1);
            d.Timing.WaitForTime(T_Repump);
            
        }
    plotindex++;
    }

    red.Disable();
  
}



