
// Ramsey scan that uses phase change instead of delay to rotate about z-axis

#include "DDScon.h"
#include "HELPERS.h"
#include <math.h>

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define qubit_transition F_Red_Carrier

#define runtime us(501)
#define timestep us(10)

//Ramsey Lock
#define quadrature_repeats 101
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


    if(SCAN){
    //Testing single Ramsey quadrature with scan ===============
        uint32_t delay=0;
        for( delay = us(0);delay <= runtime;delay=delay + timestep){
            for(loop_index = 0; loop_index < 4; loop_index ++){
                a[loop_index] = 0;
            }
            time1 = T_Qubit_Pi/2;
            time2 = delay + time1;
            time3 = T_Qubit_Pi/2 + time2;
            //Interleave repeats
            for(repeat = 0; repeat < quadrature_repeats; repeat++){
                //Loop over 4 phase quadratures
                for(quadrature = 0; quadrature < 4; quadrature++){
                    //Cooling Sequence ====================
                   // if (repeat%5==0){
                        DopplerCool(d, ir1092, blue);
                    //}

                    //turn off doppler  
                    blue.SetFreq(MHz(0));      
                    blue.Update();
                    ir1092.Disable();


                    Initialize(d, red, ir1033, ir1092, blue, 5);
                    //d.Timing.WaitForTime(us(10));
                    //End Cooling Sequence ----------------

                    //Test 4 quadratures scheme ===========
                    //Implement pi/2 gate with phase phases[TESTINGphaseselect]
                    
                    red.SetFreq(MHz(0));
                    red.Update();
                    red.Enable();

                    red.SetPhase(quadrature*8192);
                    red.SetFreq(qubit_transition);
                    d.Timing.ZeroTime();
                    red.Update();
                    d.Timing.WaitUntilTime(time1);
                    //d.Timing.WaitForTime(T_Qubit_Pi/2);
                    red.SetFreq(MHz(0));
                    red.Update();

                    //Ramsey wait
                    d.Timing.WaitUntilTime(time2);
                    //d.Timing.WaitForTime(delay);

                    //Implement pi/2 gate with phase phases[0]
                    red.SetPhase(0);
                    red.SetFreq(qubit_transition);
                    red.Update();
                    d.Timing.WaitUntilTime(time3);
                    //d.Timing.WaitForTime(T_Qubit_Pi/2);
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
                        a[quadrature]+=1;
                    }
         

                    // enable 1033
                    ir1033.Set(3);
                    d.Timing.WaitForTime(T_Repump);
                    ir1033.Set(0);
                    //End Readout --------------------------
                }
            }
            for(loop_index = 0; loop_index < 4; loop_index++){
                d.Plot.SetPoint(plotindex,a[loop_index]);
                plotindex++;
            }
        }
        red.Disable();
    }


    //End testing single Ramsey quadrature with scan -----------
   

    //Ramsey Lock ==============================================
    else{
        uint32_t ramsey_delay = 25; // in microseconds
        uint32_t ramsey_delay2 = us(ramsey_delay);
        uint32_t differential=0;
        red.SetFreq(MHz(0));
        red.Update();
        red.Enable();
        int loop = 0;
        double freqdetuning=0;
        uint32_t realfreq2=qubit_transition;

        //d.Plot.SetPoint(plotindex,realfreq*10000); plotindex++;
        //freqdetuning=RamseyLock(d, red, ir1033, ir1092, blue, 50, 251, F_Red_12_52, T_Qubit_Pi, T_Count, Count_Threshold, T_Repump);
        //d.Plot.SetPoint(plotindex,1000000 + uint32_t(freqdetuning)); plotindex++;
        //realfreq=realfreq+5000.0/2000000;
        //realfreq2=MHz(realfreq);
        //freqdetuning=RamseyLock(d, red, ir1033, ir1092, blue, 50, 251, F_Red_12_52, T_Qubit_Pi, T_Count, Count_Threshold, T_Repump);
        //d.Plot.SetPoint(plotindex,1000000 + uint32_t(freqdetuning)); plotindex++;
        
        /*
        double theta = -1.0 * 3.141593;
        uint32_t s, c;
        double t;
        int32_t s1, c1;
        for(loop = 0; loop < 1001; loop++){
            s1 = 500 * ( sin(theta));
            c1 = 500 * ( cos(theta));
            t = 1000.0 * atan2(s1, c1) / 3.146;
            theta += 2.0 * 3.141593 / 1000.0;

            d.Plot.SetPoint(plotindex,(uint32_t)(90000.0 + t)); plotindex++;
        }
        return 0 ;
        */

        for(loop = 0; loop < 1000; loop++){
        
        //realfreq2=RamseyLock(d, red, ir1033, ir1092, blue, 2500, 25, realfreq2 , T_Qubit_Pi, T_Count, Count_Threshold, T_Repump);
        realfreq2=RamseyLockIterate(d, red, ir1033, ir1092, blue, 8000, 5000, 25, realfreq2 , T_Qubit_Pi, T_Count, Count_Threshold, T_Repump,1);
        d.Plot.SetPoint(plotindex,((double)realfreq2/4294967.296)*1000000.0); plotindex++;
        //d.Plot.SetPoint(plotindex,(uint32_t)(realfreq2)); plotindex++;
}
        //d.Plot.SetPoint(plotindex,1000000 + uint32_t(freqdetuning)); plotindex++;
        //}
        
        /*
        for(loop_index = 0; loop_index < 8; loop_index ++){
            a[loop_index] = 0;
        }
        for(repeat = 0; repeat < quadrature_repeats; repeat++){
            for(differential = 1; differential < 2; differential++){
                if(differential == 0){
                    ramsey_delay2 = us(5);
                }
                else{
                    ramsey_delay2 = us(ramsey_delay);
                }

                //Set laser update times
                time1 = T_Qubit_Pi/2;
                time2 = ramsey_delay2 + time1;
                time3 = T_Qubit_Pi/2 + time2;

                //Measure each quadrature once
                for(quadrature = 0; quadrature < 4; quadrature++){
                    //Cooling Sequence ====================
                    DopplerCool(d, ir1092, blue);

                    //turn off doppler  
                    blue.SetFreq(MHz(0));      
                    blue.Update();
                    ir1092.Disable();


                    Initialize(d, red, ir1033, ir1092, blue, 5);
                    //d.Timing.WaitForTime(us(10));
                    //End Cooling Sequence ----------------

                    //Test 4 quadratures scheme ===========
                    //Implement pi/2 gate with phase phases[phaseselect]


                    red.SetPhase(8192*quadrature);
                    red.SetFreq(realfreq2);
                    d.Timing.ZeroTime();
                    red.Update();
                    d.Timing.WaitUntilTime(time1);
                    
                    //Only run if delay > 0. But do not use for delay < us(0.13)
                    //if(ramsey_delay2 != 0){ 
                        red.SetFreq(MHz(0));
                        red.Update();
                        
                        //Ramsey wait
                        d.Timing.WaitUntilTime(time2);

                        //Implement pi/2 gate with phase phases[0]
                        red.SetPhase(0);
                        red.SetFreq(realfreq2);
                        red.Update();
                    //}
                    d.Timing.WaitUntilTime(time3);
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
                        a[4*differential+quadrature]+=1;
                    }

                    // enable 1033
                    ir1033.Set(3);
                    d.Timing.WaitForTime(T_Repump);
                    ir1033.Set(0);
                    //End Readout --------------------------
                    
                   // d.Plot.SetPoint(plotindex,a[2*differential+quadrature]);
                    // plotindex++;
                }
            }
        }
        //Assume angle 0 is between -1 and +1 due to an appropriate choice of t such that delta * t < pi
        //int32_t a1 = a[0]-a[2];
        //int32_t a2 = a[3]-a[1];
        int32_t a3 = a[4]-a[6];
        int32_t a4 = a[5]-a[7];

        //d.Plot.SetPoint(plotindex,a[4]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[5]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[6]); plotindex++;
        //d.Plot.SetPoint(plotindex,a[7]); plotindex++;

        //Differential angles;
        float gate_ramsey_time_correction = 2.0 * (T_Qubit_Pi * 0.016) / 3.1416; // Multiplication by 0.016 to get units of us
        //float angleA = -1.0 * atan2(a2,a1) / 3.1416;
        
        //float angleB = 1.0 * atan2(a4,a3) / 3.1416;


        float angleB = 1.0 * atan2(a4,a3) / 3.1416;
        float deltaC = 1000000.0 * 0.5 * angleB / (1.0 * ramsey_delay);

        //d.Plot.SetPoint(plotindex,(angleA+1.0)*10000.0); plotindex++;
        //d.Plot.SetPoint(plotindex,(angleB+1.0)*10000.0); plotindex++;


        //float deltaA = 1000000.0 * 0.5 * angleB / gate_ramsey_time_correction;
        float deltaB = 1000000.0 * 0.5 * angleB / (gate_ramsey_time_correction + 1.0 * ramsey_delay);
        //float deltaC = 1000000.0 * 0.5 * angleB / (1.0 * ramsey_delay);

        
        //d.Plot.SetPoint(plotindex,90000000 + (deltaA)); plotindex++;
        
        //d.Plot.SetPoint(plotindex,1000000 + (deltaB)); plotindex++;
        
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
       
*/
       //ramsey lock with 2 sine waves (no quadratures)
       if(false){
        for(loop_index = 0; loop_index < 8; loop_index ++){
            a[loop_index] = 0;
        }
        for(repeat = 0; repeat < quadrature_repeats; repeat+=2){
            for(differential = 1; differential < 2; differential++){
                if(differential == 0){
                    ramsey_delay2 = us(5);
                }
                else{
                    ramsey_delay2 = us(ramsey_delay);
                }

                //Set laser update times
                time1 = T_Qubit_Pi/2;
                time2 = ramsey_delay2 + time1;
                time3 = T_Qubit_Pi/2 + time2;

                //Measure each quadrature once
                for(quadrature = 0; quadrature < 4; quadrature++){
                    //Cooling Sequence ====================
                    DopplerCool(d, ir1092, blue);

                    //turn off doppler  
                    blue.SetFreq(MHz(0));      
                    blue.Update();
                    ir1092.Disable();


                    Initialize(d, red, ir1033, ir1092, blue, 5);
                    //d.Timing.WaitForTime(us(10));
                    //End Cooling Sequence ----------------

                    //Test 4 quadratures scheme ===========
                    //Implement pi/2 gate with phase phases[phaseselect]


                    red.SetPhase(8192*quadrature);
                    red.SetFreq(realfreq2);
                    d.Timing.ZeroTime();
                    red.Update();
                    d.Timing.WaitUntilTime(time1);
                    
                    //Only run if delay > 0. But do not use for delay < us(0.13)
                    //if(ramsey_delay2 != 0){ 
                        red.SetFreq(MHz(0));
                        red.Update();
                        
                        //Ramsey wait
                        d.Timing.WaitUntilTime(time2);

                        //Implement pi/2 gate with phase phases[0]
                        red.SetPhase(0);
                        red.SetFreq(realfreq2);
                        red.Update();
                    //}
                    d.Timing.WaitUntilTime(time3);
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
                        a[4*differential+quadrature]+=1;
                    }

                    // enable 1033
                    ir1033.Set(3);
                    d.Timing.WaitForTime(T_Repump);
                    ir1033.Set(0);
                    //End Readout --------------------------
                    
                   // d.Plot.SetPoint(plotindex,a[2*differential+quadrature]);
                    // plotindex++;
                }
            }
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
        float deltaC = 1000000.0 * 0.5 * angleB / (1.0 * ramsey_delay);
       }
        red.Disable();
        //End Ramsey Lock -----------------------------------------
    }


}



