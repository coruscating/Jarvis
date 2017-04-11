#include "DDScon.h"
#include "HELPERS.h"
 
#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout
 
// VARIABLES
 
#define peak F_Red_12_12
#define loops 100
#define width kHz(80.0)
#define stepsize kHz(10.0)
#define freqdiff F_Red_Sideband_Diff
#define sidebandloops 150
#define initfreq 1
#define ramseylock 0
#define heatingdelay us(0)
#define sync 0 // syncing to 60 hz wall signal
#define sidebands 1 // number of sidebands on each side to scan over; 1 => 2 sidebands, 2 => 4 sidebands, etc.
#define sidebandfreq F_Red_12_12_Blue_Sideband
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
     
    int scloopsO;
    int scloopsI;
     
    uint32_t realsidebandfreq=sidebandfreq;
     
    int i=0;
    uint32_t start=0;
    uint32_t end=0;

/// from sidebandcool()
 int si=0;
                int sj=0;
int initloops=1;
int scloops=sidebandloops;
     
    Clear_mem(d);
    blue.Enable();
    ir1092.Enable();
 
    
    red.SetAmp(65000);
    red.SetFreq(0);
    red.Update();
    red.Enable();

    
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
                //realsidebandfreq=RamseyLockIterate(d, red, ir1033, ir1092, blue, 10000, 3500, 51, realsidebandfreq, T_Qubit_Pi*2, T_Count, Count_Threshold, T_Repump,1);
                
            }
        for( freq = start;freq <= end;freq = freq + stepsize){
            
            for( loop=0;loop<loops;loop++){
                //if (sync){
                //    d.Timing.WaitForSync();
                //}
                if (loop%1==0){
                    DopplerCool(d, ir1092, blue);
                } 
                ir1033.Set(0);
                ir1092.Disable();
                //Turn off doppler
                blue.SetAmp(0);
                blue.SetFreq(MHz(0));
                blue.Update();
                
                d.Timing.WaitForTime(us(10));
                //Initialize(d, red, ir1033, ir1092, blue, 5);
                //SidebandCool(d, red, ir1033, ir1092, blue, realsidebandfreq, initfreq, sidebandloops);
                 

                   for( si=0; si<5;si++){
        //Drive S-1/2 to D+3/2
        d.Timing.ZeroTime();
        red.SetFreq(F_Red_Repump);
        red.Update();
        red.SetFreq(0);
        d.Timing.WaitUntilTime(T_Polar_Pi);
        red.Update();
        //Repump
        ir1033.Set(1);
        ir1092.Enable();
        d.Timing.WaitForTime(T_Repump);
        ir1033.Set(0);
        ir1092.Disable();
        //d.Timing.WaitForTime(us(10));
    }


               

                for( si=0; si < scloops; si++){
                    sj++;
                    //Re-populate S+1/2 every initloops
                    if( sj==initloops){
                        Initialize(d, red, ir1033, ir1092, blue, 3);
                        sj=0;
                    }
                    //Pi-transition on motional sideband
                    red.SetFreq(sidebandfreq);
                    d.Timing.ZeroTime();
                    red.Update();


                    red.SetFreq(MHz(0));
                    //d.Timing.WaitUntilTime(T_Qubit_Pi/(Lamb_Dicke*sqrt(scloops-i)));
                    d.Timing.WaitUntilTime(T_Qubit_Pi);
                    red.Update();
                    //Repump
                    ir1033.Set(1);
                    ir1092.Enable();
                    d.Timing.WaitForTime(T_Repump);
                    ir1033.Set(0);
                    ir1092.Disable();
                    d.Timing.WaitForTime(us(10));
                }



                //Initialize(d, red, ir1033, ir1092, blue, 5);
                

                 for( si=0; si<5;si++){
        //Drive S-1/2 to D+3/2
        d.Timing.ZeroTime();
        red.SetFreq(F_Red_Repump);
        red.Update();
        red.SetFreq(0);
        d.Timing.WaitUntilTime(T_Polar_Pi);
        red.Update();
        //Repump
        ir1033.Set(1);
        ir1092.Enable();
        d.Timing.WaitForTime(T_Repump);
        ir1033.Set(0);
        ir1092.Disable();
        //d.Timing.WaitForTime(us(10));
    }




                //d.Timing.WaitForTime(heatingdelay);
                //turn on red for delay
                red.SetFreq(freq);
                red.Update();
                
                d.Timing.WaitForTime(us(60));
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
                   d.Plot[plotindex]+=1;
                }

                 
                // enable 1033
                ir1033.Set(1);
                d.Timing.WaitForTime(T_Repump);
                
                //d.Timing.WaitForTime(ms(1));
            }
        plotindex++;
        }
    }
    red.Disable();
 
   
}
