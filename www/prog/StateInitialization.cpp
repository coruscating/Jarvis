#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define transition F_Red_12_52
#define loops 200
#define width kHz(500.0)
#define stepsize kHz(10.0)
#define pump_transition F_Red_n12_32

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
    int i=0;
    int loops2=0;
    
	Clear_mem(d);

    blue.Enable();
    ir1092.Enable();
    red.SetAmp(A_Red);
    red.Update();
    red.Disable();
    
    
    for(i=0;i<2;i++){
    
        for( freq = transition-width;freq < transition+width;freq = freq + stepsize){
            a = 0;
            DopplerCool(d, ir1092, blue);
            for( loop=0;loop<loops;loop++) {   
                //turn off doppler         
                blue.Disable();
                ir1092.Disable();

                if (i==1){
                    red.SetFreq(pump_transition);
                    red.Update();           
                    for( loops2=0;loops2<15;loops2++) {
                        red.Enable();
                        d.Timing.WaitForTime(us(25));
                        red.Disable();
                        d.Timing.WaitForTime(us(0.01));
                        ir1033.Set(1);
                        d.Timing.WaitForTime(us(0.01));
                        ir1092.Enable();
                        d.Timing.WaitForTime(us(20));
                        ir1033.Set(0);
                        d.Timing.WaitForTime(us(0.01));
                        ir1092.Disable();
                        d.Timing.WaitForTime(us(0.01));
                    }
                }
                
                
                //turn on red for delay
                red.SetFreq(freq);
                
                red.Update();
                red.Enable();
                
                d.Timing.WaitForTime(T_Qubit_Pi);

                red.Disable();
                
                //Turn on doppler
                blue.Enable();
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



