
// Ramsey scan that uses a delay to rotate about z-axis:
// start in |0>, do pi/2 X pulse with laser detuned to f+\delta
// wait a variable delay to rotate about Z axis
// do another pi/2 pulse X pulse with detuned laser
// same as normal ramsey scan, just with large detuning to quickly
// check if we're on the right frequency

#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_Repump
//#define qubit_transition F_Red_Carrier
#define loops 200
#define runtime us(2000.0)
#define timestep us(20.0)
#define detuning kHz(0)
#define ramseylock 0

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    int plotindex=0;
    uint32_t delay=0;
    int loop=0;
    int count=0;
    d.Pmt0.Enable();
    uint32_t pmtcounts=0;
    uint32_t time1=0;
    uint32_t time2=0;
    uint32_t realfreq2=qubit_transition;
    uint32_t realfreq=qubit_transition;

	InitScript(d,red,ir1033,ir1092,blue);

    uint32_t delta = 2500;
    for( delay = us(0);delay <= runtime;delay=delay + timestep){
        a = 0;
        if (ramseylock==1){
            if(plotindex < 4){
                delta = 2500 - plotindex * 500;
            }
            else{
                delta = 500;
            }
            realfreq2=RamseyLockIterate(d, red, ir1033, ir1092, blue, delta, delta, 25, realfreq2, T_Polar_Pi, T_Count, Count_Threshold, T_Repump, 1);
            realfreq=realfreq2+detuning;
        } 
        else {
            realfreq=qubit_transition+detuning;
        }

        for( loop=0;loop<loops;loop++) {

            if (loop%10==0){
                DopplerCool(d, ir1092, blue);
            }


            //turn off doppler  
            blue.SetFreq(MHz(0));      
            blue.Update();
            ir1092.Disable();


            //Initialize(d, red, ir1033, ir1092, blue, 5);

            if (delay!=us(0)){
                time1=T_Polar_Pi/2+delay;
                time2=T_Polar_Pi+delay;

                red.SetFreq(realfreq);


                d.Timing.ZeroTime();
                red.Update();
                
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(T_Polar_Pi/2);
                red.Update();
                
                red.SetFreq(realfreq);
                d.Timing.WaitUntilTime(time1);
                red.Update();
                
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(time2);
                red.Update();
            } else {
                red.SetFreq(realfreq);
                d.Timing.ZeroTime();
                red.Update();
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(T_Polar_Pi);
                red.Update();
            }

            
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



