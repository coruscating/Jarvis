#pragma once

#include "DDScon.h"
#include "/Dropbox (MIT)/Quanta/Software/GitHub/DeviceWorkers/ddslib/HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define peak MHz(123.4)
#define loops 200
#define width MHz(1)
#define stepsize kHz(10.0)
#define redpower 51000
#define stateprep 1

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
    
	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();

    red.SetAmp(redpower);
    red.Update();
    red.Disable();
    
    d.Write(120);

    d.Pmt0.ClearCorr();
    for( freq = peak-width;freq <= peak + width;freq += stepsize){
            d.Pmt0.SyncCorr();
            ir1033.Set(2);
            d.Timing.WaitForTime(us(180));
            //d.Timing.WaitForSync();
            ir1033.Set(0);
            //d.Timing.WaitForTime(ms(1));
        }

    //red.Disable();
  
}



