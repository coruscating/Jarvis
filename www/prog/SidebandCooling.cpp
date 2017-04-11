#include "DDScon.h"
#include "HELPERS.h"
 
#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout
 
// VARIABLES
 
#define peak F_Red_Carrier
#define loops 200
#define width kHz(30.0)
#define stepsize kHz(5.0)
#define freqdiff F_Red_Sideband_Diff
#define sidebandloops 100
#define initfreq 3 // this is the power of two that is the period for initialization. For example 3 means once every 2^3=8 loops
#define ramseylock 1
#define heatingdelay us(0)
#define sync 0 // syncing to 60 hz wall signal
#define sidebands 1 // number of sidebands on each side to scan over; 1 => 2 sidebands, 2 => 4 sidebands, etc.
#define sidebandfreq F_Red_12_52_Red_Sideband
// END VARIABLES
 
int main()
{
    DDScon d;
    int plotindex=0;
    uint32_t freq=0;
    int loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
     
    uint32_t realcarrierfreq=peak;
    int i=0;
    uint32_t start=0;
    uint32_t end=0;
     
    InitScript(d,red,ir1033,ir1092,blue);

    int scloops[sidebandloops];

    //int *scloops=SidebandCalc(sidebandloops);
    for( i=0; i < sidebandloops; i++){
        scloops[i]=(uint32_t)(T_Qubit_Pi/((float)Lamb_Dicke*sqrt(sidebandloops-i)));
    }


    for(i=-sidebands;i<=sidebands;i++){
        // only detect at the two sidebands and skip over the carrier to save us time
        if(i==0){
            continue;
        }
        else{
            start=peak + i*freqdiff - width;
            end=peak + i*freqdiff + width;
        }
        if (ramseylock==1){
                // carrier has more contrast, better for the lock
                realcarrierfreq=RamseyLockIterate(d, red, ir1033, ir1092, blue, 20000, 3500, 51, realcarrierfreq, T_Qubit_Pi, T_Count, Count_Threshold, T_Repump,1);
            }
        for( freq = start;freq <= end;freq = freq + stepsize){
            
            for( loop=0;loop<loops;loop++){
                //if (sync){
                //    d.Timing.WaitForSync();
                //}
                if (loop>>1<<1==0){
                    DopplerCool(d, ir1092, blue);
                } 
                ir1033.Set(0);
                ir1092.Disable();
                //Turn off doppler
                blue.SetAmp(0);
                blue.SetFreq(MHz(0));
                blue.Update();

                //Initialize(d,red,ir1033,ir1092,blue,5);
                SidebandCool(d, red, ir1033, ir1092, blue, realcarrierfreq+freqdiff, initfreq, sidebandloops,scloops);
                Initialize(d,red,ir1033,ir1092,blue,5);

                //d.Timing.WaitForTime(heatingdelay);
                //turn on red for delay
                red.SetFreq(freq);
                d.Timing.ZeroTime();
                red.Update();
                
                
                red.SetFreq(0);
                d.Timing.WaitUntilTime(us(71));
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
                   d.Plot[plotindex]+=1;
                }

                // enable 1033
                ir1033.Set(3);
                d.Timing.WaitForTime(T_Repump);
            }
        plotindex++;
        }
    }
    red.Disable();
 
   
}
