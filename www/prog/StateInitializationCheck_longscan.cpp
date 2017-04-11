#include "DDScon.h"
#include "HELPERS.h"

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


#define loops 500
#define Ninitloops 1000

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    int plotindex=0;
    uint32_t freq=0;
    int loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    
   
    
    int initloops = 0;

    
    
    int i=0;
    double startfreq=0;
    double endfreq=0;
    uint32_t start=0;
    uint32_t end=0;
    
    Clear_mem(d);
    blue.Enable();
    ir1092.Enable();

    red.SetFreq(0);
    red.SetAmp(A_Red);
    red.Update();
    red.Enable();
    

    for( initloops=0;initloops<Ninitloops;initloops++){
            a = 0;
            DopplerCool(d, ir1092, blue);
            d.Timing.WaitForTime(us(1000));
            d.Write(initloops);
            for( loop=0;loop<loops;loop++){

                //Turn off doppler
                blue.SetAmp(0);
                blue.SetFreq(MHz(0));
                blue.Update();
                ir1092.Disable();
                d.Timing.WaitForTime(us(10));

                
                Initialize(d,red,ir1033,ir1092,blue,3);


                d.Timing.ZeroTime();
                red.SetFreq(F_Red_Repump);
                red.Update();
                
                d.Timing.WaitUntilTime(T_Polar_Pi);
                red.SetFreq(0);
                red.Update();
                
                //Turn on doppler
                blue.SetAmp(A_Blue_Det);
                blue.SetFreq(F_Blue_Det);
                blue.Update();
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



