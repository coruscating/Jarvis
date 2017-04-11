#include "DDScon.h"
#include "HELPERS.h"


// rabi flops at set frequency


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define stateprep 0
#define sidebandcool 0
#define runtime us(50.0)
#define timestep us(0.5)
#define loops 100
#define qubit_transition F_Red_n12_32

#define sidebandloops 50
#define initfreq 3
#define ramseylock 0
#define sync 0

int main()
{
    // Initialize:
    DDScon d;
    //red.Disable();
    int plotindex=0;
    uint32_t time=0;
    int loop=0;
    int loops2=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
    uint32_t realfreq=qubit_transition; //qubit_transition;

    
	Clear_mem(d);
    blue.Enable();
    ir1092.Enable();
    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();

    //InitScript(d,red,ir1033,ir1092,blue);

    int scloops[sidebandloops];

    if (sidebandcool==1){
        for( i=0; i < sidebandloops; i++){
            scloops[i]=(uint32_t)(T_Qubit_Pi/((float)Lamb_Dicke*sqrt(sidebandloops-i)));
        }
    }

    for( time = us(0);time <= runtime;time=time+timestep){
            if (ramseylock==1){  
                realfreq=RamseyLockIterate(d, red, ir1033, ir1092, blue, 20000, 3500, 51, realfreq, T_Qubit_Pi, T_Count, Count_Threshold, T_Repump,1);
            }

        for( loop=0;loop<loops;loop++) {
            /*if (sync){
                d.Timing.WaitForSync();
            }*/
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
            if (sidebandcool==1){
                SidebandCool(d, red, ir1033, ir1092, blue, realfreq+F_Red_Sideband_Diff, initfreq, sidebandloops,scloops);
            }

            if(time != us(0)){
                if (ramseylock==1){
                    red.SetFreq(realfreq);
                } else {
                    red.SetFreq(qubit_transition);
                }
                d.Timing.ZeroTime();
                red.Update();  

                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(time);
                red.Update();
            }

            //Turn on doppler
            blue.SetFreq(F_Blue_Det);
            blue.SetAmp(A_Blue_Det);
            blue.Update();
            //ir1092.SetAmp(65000);
            ir1092.Update();
            ir1092.Enable();
            
            
            //a+=StateDetection(d,ir1092,blue);


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
            
        }
    plotindex++;
    }
    

    red.Disable();
    ir1033.Set(0);

}



