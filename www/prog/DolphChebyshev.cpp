#include "DDScon.h"
#include "HELPERS.h"


// rabi flops at set frequency


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define stateprep 1
#define sidebandcool 0
#define runtime T_Qubit_Pi*4
#define timestep us(0.5)/5
#define loops 100
#define qubit_transition F_Red_Carrier
#define stateprep_transition F_Red_Repump

#define sidebandloops 190
#define initfreq 3

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    uint32_t plotindex=0;
    int time=0;
    int loop=0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;

    uint32_t pulses[5]={6375,29748,0,29748,6375};
    //uint32_t pulses[5]={18193,28894,0,3874,14574};
    //uint32_t pulses[9]={12379,23521,24734,30024,0,2742,8033,9245,20388};
    //uint16_t pulses[3]={9612,0,23156};
    //uint16_t pulses[3]={0,8192,0};
    //uint16_t pulses[5]={0,13653,5461,13653,0};
    //uint32_t pulses[5]={0,0,0,0,0};
    int j=0;    

    Clear_mem(d);
    blue.Enable();
    ir1092.Enable();
    red.SetAmp(A_Red);
    red.SetFreq(0);
    red.SetPhaseCoherent();
    red.Update();
    red.Enable();

    for( time = us(0);time <= runtime;time=time + timestep){
        a = 0;

        for( loop=0;loop<loops;loop++) {
            if (loop%1==0){
            DopplerCool(d, ir1092, blue);
            }
            //turn off doppler        
            blue.SetFreq(0);
            blue.Update();
            ir1092.Disable();
            ir1033.Set(0);


            if (stateprep==1){
                Initialize(d,red,ir1033,ir1092,blue,5);
            }
            if (sidebandcool==1){
                SidebandCool(d, red, ir1033, ir1092, blue, initfreq, sidebandloops);
                Initialize(d,red,ir1033,ir1092,blue,3);
                /*ir1092.Enable();
                ir1033.Set(1);
                d.Timing.WaitForTime(us(100));
                ir1033.Set(0);
                ir1092.Disable();*/
            }


            red.SetFreq(qubit_transition);
            red.Update();
            d.Timing.ZeroTime();
            for(j=0;j<5;j++){                
                red.SetPhase(pulses[j]);
                d.Timing.WaitUntilTime(time*j);
                red.Update();
            }
            /*red.SetPhase(6375);
            red.Update();
            d.Timing.WaitForTime(time);
            red.SetPhase(29748);
            red.Update();
            d.Timing.WaitForTime(time);
            red.SetPhase(0);
            red.Update();
            d.Timing.WaitForTime(time);
            red.SetPhase(29748);
            red.Update();
            d.Timing.WaitForTime(time);
            red.SetPhase(6375);
            red.Update();
            d.Timing.WaitForTime(time);*/
            
            red.SetFreq(0);
            red.SetPhase(0);
            d.Timing.WaitUntilTime(time*(j+1));
            red.Update();
            //red.Update();
            //Turn on doppler
            blue.SetFreq(F_Blue_Det);
            blue.SetAmp(A_Blue_Det);
            blue.Update();
            //ir1092.SetAmp(65000);
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
            //d.Timing.WaitForTime(ms(1));
        }
    d.Plot.SetPoint(plotindex,a);
    plotindex++;
    }
    

    red.Disable();

}



