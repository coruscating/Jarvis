
// Ramsey scan that uses a delay to rotate about z-axis:
// start in |0>, do pi/2 X pulse with laser detuned to f+\delta
// wait a variable delay to rotate about Z axis
// do another pi/2 pulse X pulse with detuned laser
// result should be sin^2(\delta t)

#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_Carrier
#define loops 200
#define runtime us(20)
#define timestep us(1)
#define detuning kHz(10)

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
	Clear_mem(d);

    blue.Enable();
    ir1092.Enable();


    red.SetPhaseCoherent();
    //red.SetPhaseContinuous();

    red.SetAmp(A_Red);
    red.SetFreq(0);
    red.Update();
    red.Enable();
    int i =0;

    for(i=0;i<=15;i++){


    delay=us(0);
    for( delay = us(0);delay <= runtime;delay=delay + timestep){
        a = 0;
        for( loop=0;loop<loops;loop++) {

            if (loop%2==0){
                DopplerCool(d, ir1092, blue);
            }


            //turn off doppler  
            blue.SetFreq(MHz(0));      
            blue.Update();
            ir1092.Disable();


            Initialize(d, red, ir1033, ir1092, blue, 5);

            if (delay!=us(0)){
                time1=T_Qubit_Pi/2+delay;
                time2=T_Qubit_Pi+delay;

                red.SetFreq(qubit_transition+detuning);
                d.Timing.ZeroTime();
                red.Update();
                
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(T_Qubit_Pi/2);
                red.Update();
                
                red.SetFreq(qubit_transition+detuning);
                d.Timing.WaitUntilTime(time1);
                red.Update();
                
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(time2);
                red.Update();
            } else {
                red.SetFreq(qubit_transition+detuning);
                d.Timing.ZeroTime();
                red.Update();
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(T_Qubit_Pi);
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
}
    red.Disable();

}



