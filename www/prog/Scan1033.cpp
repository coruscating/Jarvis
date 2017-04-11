#include "DDScon.h"
#include "HELPERS.h"


// trying to optimize 1033 repump time


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define stateprep 0
#define sidebandcool 0
#define loops 500
#define qubit_transition F_Red_12_52
#define stateprep_transition F_Red_n12_32

#define sidebandloops 190
#define initfreq 3

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    int plotindex=0;
    int loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
    int repump_time=0;
    
	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();
    red.SetAmp(A_Red);
    red.Update();
    red.Disable();

    for(repump_time=us(0);repump_time<us(10);repump_time=repump_time+us(1)){

        a = 0;

        for( loop=0;loop<loops;loop++) {
            if (loop%1==0){
            DopplerCool(d, ir1092, blue);
            }
            //turn off doppler        
            blue.SetFreq(MHz(0));
            blue.Update();
            ir1092.Disable();
            ir1033.Set(0);

        

            if (stateprep==1){
                Initialize(d,red,ir1033,ir1092,blue,5);
            }

            red.SetFreq(qubit_transition);
            red.Update();
            //turn on red for time[time]
            red.Enable();       
            d.Timing.WaitForTime(T_Qubit_Pi);
            red.Disable();
            ir1033.Set(1);
            d.Timing.WaitForTime(repump_time);
            ir1033.Set(0);
            //Turn on doppler
            blue.SetFreq(F_Blue_Det);
            blue.SetAmp(A_Blue_Det);
            blue.Update();
            //ir1092.SetAmp(65000);
            ir1092.Update();
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
            d.Timing.WaitForTime(repump_time);
            //d.Timing.WaitForTime(ms(1));
        }
    d.Plot.SetPoint(plotindex,a);
    plotindex++;
    
}
    red.Disable();

}



