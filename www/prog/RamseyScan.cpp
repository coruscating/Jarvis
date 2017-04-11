
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
#define loops 100
#define runtime us(1000.0)
#define timestep us(1.0)
#define detuning kHz(10)
#define ramseylock 0
#define stateprep 1

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
    uint32_t realfreq2=F_Red_Carrier;
    uint32_t realfreq=F_Red_Carrier;

	Clear_mem(d);

    blue.Enable();
    ir1092.Enable();


    red.SetPhaseCoherent();
    //red.SetPhaseContinuous();

    red.SetAmp(A_Red);
    red.SetFreq(0);
    red.Update();
    red.Enable();

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
            realfreq2=RamseyLockIterate(d, red, ir1033, ir1092, blue, delta, delta, 25, realfreq2, T_Qubit_Pi, T_Count, Count_Threshold, T_Repump,1);
            realfreq=realfreq2+detuning;
        } 
        else {
            realfreq=qubit_transition+detuning;
        }

        for( loop=0;loop<loops;loop++) {

            if (loop%2==0){
                //DopplerCool(d, ir1092, blue);

                int pmt_counts=0;
                double freq=A_Blue_Start;
                double power=A_Blue_Start;
                const double dpower=(A_Blue_Start-A_Blue_End)/N_Blue_Steps;
                const double dfreq= (F_Blue_End-F_Blue_Start)/N_Blue_Steps;
                d.Pmt0.Clear();

                blue.SetPhaseContinuous();
                ir1092.SetAmp(A_1092_Doppler);
                ir1092.Update();
                ir1092.Enable();

                
                for(freq=F_Blue_Start;freq<=F_Blue_End;freq=freq+dfreq){
                    blue.SetFreq(freq);
                    blue.SetAmp(power);
                    blue.Update();
                    d.Timing.WaitForTime(T_Blue_Step);
                    power=power-dpower;
                }

            }


            //turn off doppler  
            blue.SetFreq(MHz(0));      
            blue.Update();
            ir1092.Disable();

            if(stateprep){
                Initialize(d, red, ir1033, ir1092, blue, 5);
            }
            if (delay!=us(0)){
                time1=T_Qubit_Pi/2+delay;
                time2=T_Qubit_Pi+delay;

                red.SetFreq(realfreq);


                d.Timing.ZeroTime();
                red.Update();
                
                red.SetFreq(MHz(0));
                d.Timing.WaitUntilTime(T_Qubit_Pi/2);
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

    red.Disable();

}



