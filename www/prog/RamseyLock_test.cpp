
// Ramsey scan that uses phase change instead of delay to rotate about z-axis

#include "DDScon.h"
#include "HELPERS.h"
#include <math.h>

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_12_52

#define runtime us(500)
#define timestep us(10)

//Ramsey Lock
#define quadrature_repeats 251
#define quadrature_time us(100)
//For testing purposes
#define SCAN false
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

    //Ramsey Lock
    //d.Timing.ZeroPhase();
    uint32_t repeat = 0;  // Loop index
    uint32_t quadrature = 0; // Loop index
    uint32_t loop_index = 0; // Loop index
    int plotindex=0;

    uint32_t time1 = 0; 
    uint32_t time2 = 0;
    uint32_t time3 = 0;
    
    uint32_t a[8] = {0};

    //Ramsey Lock ==============================================
    else{
        uint32_t ramsey_delay = 50; // in microseconds
        uint32_t ramsey_delay2 = us(ramsey_delay);
        uint32_t differential=0;
        float frequency=0;
        red.SetFreq(MHz(0));
        red.Update();
        red.Enable();
        int loop = 0;
        for(loop = 0; loop < 200; loop++){
            plotindex++
        for(loop_index = 0; loop_index < 8; loop_index ++){
            a[loop_index] = 0;
        }
            frequency = RamseyLock(d,red,ir1092,ir1033,blue,ramsey_delay,
                        quadrature_repeats,qubit_transition);

            d.Plot.SetPoint(plotindex,frequency+90000)
        }
        //Assume angle 0 is between -1 and +1 due to an appropriate choice of t such that delta * t < pi
        //int32_t a1 = a[0]-a[2];
        //int32_t a2 = a[3]-a[1];
        int32_t a3 = a[4]-a[6];
        int32_t a4 = a[7]-a[5];

        //d.Plot.SetPoint(plotindex,a[4]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[5]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[6]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[7]); plotindex++;

        //Differential angles;
        float gate_ramsey_time_correction = 2.0 * (T_Qubit_Pi * 0.016) / 3.1416; // Multiplication by 0.016 to get units of us
        //float angleA = -1.0 * atan2(a2,a1) / 3.1416;
        float angleB = -1.0 * atan2(a4,a3) / 3.1416;

        //d.Plot.SetPoint(plotindex,(angleA+1.0)*10000.0); plotindex++;
        //d.Plot.SetPoint(plotindex,(angleB+1.0)*10000.0); plotindex++;


        //float deltaA = 1000000.0 * 0.5 * angleB / gate_ramsey_time_correction;
        float deltaB = 1000000.0 * 0.5 * angleB / (gate_ramsey_time_correction + 1.0 * ramsey_delay);
        //float deltaC = 1000000.0 * 0.5 * angleB / (1.0 * ramsey_delay);

        
        //d.Plot.SetPoint(plotindex,90000000 + (deltaA)); plotindex++;
        d.Plot.SetPoint(plotindex,90000000 + (deltaB)); plotindex++;
        //d.Plot.SetPoint(plotindex,90000000 + (deltaC)); plotindex++;

        //Evaluate contrast
        //d.Plot.SetPoint(plotindex, sqrt(a3 * a3 + a4 * a4)); plotindex++;
    
     
        //float angle0 = angleB - angleA; //This is between -2 and +2 by using an approximate value of 3.1416 < Pi
        //float angle1 = 100.0 * (float)(((int32_t)(10000.0*(1.0+angle0)) % 20000) - 10000); // --1000 to 1000
        //uint32_t frequency = (uint32_t) (90000000.0 + (float)angle1 / (float)(ramsey_delay) );
        //We want Mod(angle in radians, 2pi, -pi)
        //d.Plot.SetPoint(plotindex,frequency);

        //d.Plot.SetPoint(loop,(uint32_t)(10000.0*(1.01+atan2(a[2]-a[0],-a[3]+a[1])/3.14159))); //== (delta * delay + 2 * delta / Rabi_frequency)
        //d.Timing.WaitForTime(ms(800));
        //uint32_t (uint32_t)(32768.0*atan2(a[2]-a[0],a[3]-a[1]));
        
       }
        red.Disable();
        //End Ramsey Lock -----------------------------------------
    }


}



