#include "DDScon.h"



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
    int plotindex=1;
    uint32_t freq=0;
    int loops=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    
    uint32_t time=0;
    
    
	for(count=0;count<3500;count++){
	d.Plot.SetPoint(count,0);
	}


    for( time=us(0.1);time<=us(10);time+=us(0.1)){
        a = 0;
        for( loops=0;loops<10000;loops++) {
            ir1092.Enable();

            d.Timing.WaitForTime(ms(1));
            
            
            ir1092.Disable();
            d.Timing.WaitForTime(time);
            
            
            //count
            d.Pmt0.Clear();
            d.Timing.WaitForTime(us(1));
            pmtcounts=d.Pmt0.GetCount();
            a+=pmtcounts;
            

        }
    d.Plot.SetPoint(plotindex,a);
    plotindex++;
    }

    ir1092.Enable(); 
}



