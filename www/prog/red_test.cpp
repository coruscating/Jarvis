// testing script to see if pulse programmer is working properly


#pragma once

#include "DDScon.h"
#include "/Dropbox (MIT)/Quanta/Software/GitHub/DeviceWorkers/ddslib/HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define peak F_Red_n12_32
#define loops 100
#define width kHz(100.0)
#define stepsize kHz(1.0)

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
    int i=0;
    
//for( l=0;l<loops;l++) {
  // d.Digout.Set(6);

    ir1092.SetFreq(MHz(200));
    ir1092.SetAmp(65000);
    ir1092.Update();
    ir1092.Enable();
  //  d.Timing.WaitForTime(us(50));
   // ir1092.Disable();
   // d.Digout.Set(0);
    //d.Timing.WaitForTime(us(50));
            
//}

	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();

    red.SetAmp(65000);
    
    red.Update();
    red.Disable();
    red.SetFreq(MHz(120));
    red.SetPhaseContinuous();
    //blue.SetPhaseCoherent();
        for( l=0;l<loops;l++) {
        a = 0;
        d.Digout.Set(3);
        d.Timing.WaitForTime(us(10));
        d.Digout.Set(0);
        DopplerCool(d, ir1092, blue);

                    
            //turn off doppler      
            blue.Disable();
            //__delay();
            ir1092.Disable();
            d.Timing.WaitForTime(us(50));
            d.Timing.WaitForTime(us(10));

            red.Enable();  

            for (i=-2;i<=2;i++){
            //turn on red for delay
        
            red.SetAmp(60000);
            red.Update();
                   
            d.Timing.WaitForTime(us(10));
            }
            red.Disable();
            
            //__delay();
            //d.Timing.WaitForTime(us(100));
            
            //Turn on doppler
            blue.Enable();
            blue.SetAmp(60000);
            blue.Update();
            d.Timing.WaitForTime(us(10));
            blue.Disable();
            //__delay();
            
            ir1092.Enable();

            
            //count
            d.Pmt0.Clear();
            d.Timing.WaitForTime(us(10));
            pmtcounts=d.Pmt0.GetCount();
            if (pmtcounts <= Count_Threshold){
               a+=1;
               }
            else{
               a+=0;
               }
            
            
            
            // enable 1033
            //ir1033.Set(1);
            //d.Timing.WaitForTime(T_Repump);
            //ir1033.Set(0);
        }



}