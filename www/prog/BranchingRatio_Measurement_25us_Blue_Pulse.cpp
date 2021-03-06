#include "DDScon.h"
#include "HELPERS.h"

// WORKING VERSION

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout



#define qubit_transition F_Red_12_12
#define FRepump F_Red_n12_n12


int main()
{
    // Initialize:
    DDScon d;

    //red.Disable();
    int plotindex=0;
    uint32_t loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
    Clear_mem(d);
    uint32_t SPCounts=0;
    uint32_t ResetCounts=0;
    uint32_t Scattered_counts=0;
    uint32_t Dark_counts=0;
    uint32_t counts=0;

    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();
    ir1033.Set(0);

    d.Pmt0.ClearCorr();

    for( loop=0;loop<branching_ratio_loops;loop++) {      

        d.Plot[loop-(loop>>11<<11)]=DopplerCool(d,ir1092,blue);

        // mark what loop we are on
        d.Write(loop); 
        //Turn off doppler
        blue.SetAmp(0);
        blue.SetFreq(0);
        blue.Update();

        ir1092.SetAmp(A_1092_Det);
        ir1092.SetFreq(F_1092_Det);
        ir1092.Update();
        //Prepare in S state
        d.Timing.WaitForTime(us(10));
        ir1092.Disable();
        d.Timing.WaitForTime(us(1));

        
        //Prepare for measurement
        blue.SetAmp(branching_ratio_amp);
        blue.SetFreq(branching_ratio_detuning);
        
        //Count photons until ion is shelved

        d.Timing.ZeroTime();
        d.Pmt0.SyncCorr().Clear();
        blue.Update(); 

        blue.SetFreq(MHz(0));
        d.Timing.WaitUntilTime(us(25));
        blue.Update();
        
        blue.SetFreq(F_Blue_Det);
        //Calibrate scattered counts   
        d.Timing.WaitUntilTime(us(26));
        blue.Update();

        blue.SetFreq(0);
        d.Timing.WaitUntilTime(us(51));
        blue.Update();


        d.Timing.WaitUntilTime(us(52));
        ir1092.Enable();
        d.Timing.WaitUntilTime(us(57.5));
        ir1092.Disable();
        d.Timing.WaitUntilTime(us(58.5));
        ir1092.Enable();
        d.Timing.WaitUntilTime(us(64));
        ir1092.Disable();
    }

    DopplerCool(d,ir1092,blue);
    blue.SetFreq(F_Blue_End);
    blue.SetAmp(A_Blue_End);
    blue.Update();
    red.Disable();
    ir1033.Set(0);

}



