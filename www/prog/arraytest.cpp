
// Ramsey scan that uses phase change instead of delay to rotate about z-axis

#include "DDScon.h"
#include "HELPERS.h"
#include <math.h>

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_12_52

#define runtime us(200)
#define timestep us(10)

//Ramsey Lock
#define quadrature_repeats 2
#define quadrature_time us(100)
//For testing purposes
#define TESTINGphaseselect 3 //choose phases[0,1,2,3]
#define TESTING false

int main()
{
    // Initialize:
    DDScon d;
    //red.Disable();
    int count=0;
    d.Pmt0.Enable();
    uint32_t pmtcounts=0;

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

    uint16_t phases[4] = {0,8192,16384,24576}; // pulses at phase 0,pi/4,pi/2,3pi/4


    //End testing single Ramsey quadrature with scan -----------
    

    //Ramsey Lock ==============================================
    uint32_t a[8] = {0};
    uint32_t repeat = 0;
    uint32_t quadrature = 0;
    uint32_t ramsey_delay = 10; // in microseconds
    uint32_t ramsey_delay2 = us(ramsey_delay);
    uint32_t differential=0;
    int plotindex=0;

    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();
    for(differential = 0; differential < 2; differential++){
        if(differential == 0){
            ramsey_delay2 = us(0);
        }
        else{
            ramsey_delay2 = us(ramsey_delay);
        }
        for(quadrature = 0; quadrature < 4; quadrature++){
            a[2*differential+quadrature] = 0;
            for(repeat = 0; repeat < quadrature_repeats; repeat++){
                //Cooling Sequence ====================
                if (repeat%5==0){
                    DopplerCool(d, ir1092, blue);
                }
/*
                //turn off doppler  
                blue.SetFreq(MHz(0));      
                blue.Update();
                ir1092.Disable();


                Initialize(d, red, ir1033, ir1092, blue, 5);*/
                //d.Timing.WaitForTime(us(10));
                //End Cooling Sequence ----------------

                //Test 4 quadratures scheme ===========
                //Implement pi/2 gate with phase phases[phaseselect]
d.Plot.SetPoint(plotindex,phases[quadrature]);
                /*red.SetPhase(phases[quadrature]);

                red.SetFreq(qubit_transition);
                red.Update();
                red.Enable();
                d.Timing.WaitForTime(T_Qubit_Pi/2);
                red.SetFreq(MHz(0));
                red.Update();

                //Ramsey wait
                d.Timing.WaitForTime(ramsey_delay2);

                //Implement pi/2 gate with phase phases[0]
                red.SetPhase(0);
                red.SetFreq(qubit_transition);
                
                red.Update();
                d.Timing.WaitForTime(T_Qubit_Pi/2);
                red.SetFreq(MHz(0));
                red.Update();
                //EndTest 4 quadratures scheme --------
                
                //Readout =============================
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
                    a[2*differential+quadrature]+=1;
                }

                // enable 1033
                ir1033.Set(1);
                d.Timing.WaitForTime(T_Repump);
                ir1033.Set(0);
                //End Readout --------------------------*/
            }
            
            plotindex++;
        }
    }

    
   
    red.Disable();
    //End Ramsey Lock -----------------------------------------



}



