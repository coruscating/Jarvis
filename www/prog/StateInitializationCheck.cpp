#include "DDScon.h"
#include "HELPERS.h"

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


#define loops 500
#define Ninitloops 100

int main()
{
    // Initialize:
    DDScon d;
    //red.Disable();
    int plotindex=0;
    int loop=0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    
   
    uint32_t a=0;
    int initloops = 0;

    
    Clear_mem(d);
    blue.Enable();
    ir1092.Enable();
    ir1033.Set(0);

    red.SetFreq(0);
    red.SetAmp(A_Red);
    red.Update();
    red.Enable();

    

    for( initloops=0;initloops<Ninitloops;initloops++){

            
a=0;
            for( loop=0;loop<loops;loop++){
                if(loop%1==0){
                    DopplerCool(d, ir1092, blue);
                }
                ir1033.Set(0);
                //Turn off doppler
                blue.SetAmp(0);
                blue.SetFreq(MHz(0));
                blue.Update();
                d.Timing.WaitForTime(us(2));
                ir1092.Disable();
                d.Timing.WaitForTime(us(10));

                
                Initialize(d,red,ir1033,ir1092,blue,initloops);


                
                //Pi pulse on polar line
                d.Timing.ZeroTime();
                red.SetFreq(F_Red_Repump);
                red.Update();
                
                d.Timing.WaitUntilTime(T_Polar_Pi);
                red.SetFreq(0);
                red.Update();

                /*d.Timing.ZeroTime();
                //Pi pulse on polar line
                red.SetFreq(F_Red_Carrier);
                red.Update();

                d.Timing.WaitUntilTime(T_Polar_Pi);
                red.SetFreq(0);
                red.Update();*/
                
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
                    //d.Plot[plotindex]+=1;
                    a+=1;
                }
        
                
                // enable 1033
                ir1033.Set(1);
                d.Timing.WaitForTime(T_Repump);
      

            }
            d.Plot.SetPoint(plotindex,a);
        plotindex++;
    }
    red.Disable();

  
}



