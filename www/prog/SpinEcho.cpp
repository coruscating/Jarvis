
// Ramsey scan that uses phase change instead of delay to rotate about z-axis

#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_12_52
#define loops 200
#define runtime us(800)
#define timestep us(2)

int main()
{
    // Initialize:
    DDScon d;
    uint16_t a=0;
    //red.Disable();
    int plotindex=0;
    uint16_t delay=0;
    int loop=0;
    int count=0;
    d.Pmt0.Enable();
    uint16_t pmtcounts=0;

	Clear_mem(d);

    blue.Enable();
    ir1092.Enable();

    //red.SetFreq(qubit_transition+kHz(5));
    red.SetPhaseCoherent();
    //red.SetPhaseContinuous();
    //d.Timing.ZeroPhase();
    red.SetAmp(A_Red);
    red.Update();
    red.Disable();


    for( delay = us(0);delay <= runtime;delay=delay + timestep){
        a = 0;
        for( loop=0;loop<loops;loop++) {

            if (loop%5==0){
                DopplerCool(d, ir1092, blue);
            }


            //turn off doppler  
            blue.SetFreq(MHz(0));      
            blue.Update();
            ir1092.Disable();


            Initialize(d, red, ir1033, ir1092, blue, 5);
            //d.Timing.WaitForTime(us(10));



            //turn on red for time[time]
            red.SetFreq(qubit_transition+kHz(20));
            red.Update();
            red.Enable();
            d.Timing.WaitForTime(T_Qubit_Pi/2);
            //red.Disable();
            
            
            red.SetFreq(MHz(0));
            red.Update();

            d.Timing.WaitForTime(us(10));
            red.SetFreq(qubit_transition+kHz(20));
            red.Update();
            d.Timing.WaitForTime(T_Qubit_Pi);
            red.SetFreq(MHz(0));
            red.Update();
            
            d.Timing.WaitForTime(delay);

            red.SetFreq(qubit_transition+kHz(20));
            red.Update();
            d.Timing.WaitForTime(T_Qubit_Pi/2);
            //red.Disable();
            red.SetFreq(MHz(0));
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



