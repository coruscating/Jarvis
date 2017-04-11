#include "DDScon.h"
#include "HELPERS.h"

// WORKING VERSION

#define blue408 d.Ch1
#define blue422 d.Ch0
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

    

    d.Pmt0.ClearCorr();
    blue408.SetFreq(MHz(180));
    blue408.SetAmp(15000);
    blue408.SetPhaseContinuous();
    blue408.Update();
    blue408.Disable();

    for( loop=0;loop<branching_ratio_loops;loop++) {      

        d.Plot[loop-(loop>>11<<11)]=DopplerCool(d,ir1092,blue422);

        // mark what loop we are on
        d.Write(loop); 
        //Turn off doppler
        blue422.SetAmp(0);
        blue422.SetFreq(0);
        blue422.Update();

        ir1092.SetAmp(A_1092_Det);
        ir1092.SetFreq(F_1092_Det);
        ir1092.Update();
        ir1033.Set(1);
        //Prepare in S state
        d.Timing.WaitForTime(us(10));
        ir1092.Disable();
        ir1033.Set(0);
        d.Timing.WaitForTime(us(1));

        
        //Prepare for measurement
        blue422.SetAmp(branching_ratio_amp);
        blue422.SetFreq(branching_ratio_detuning);

        
        //Count photons until ion is shelved

        d.Timing.ZeroTime();
        d.Pmt0.SyncCorr().Clear();
        blue408.Enable();

        d.Timing.WaitUntilTime(us(20));
        blue408.Disable();

        d.Timing.WaitUntilTime(us(21));
        blue408.Enable();

        d.Timing.WaitUntilTime(us(41));
        blue408.Disable();

        d.Timing.WaitUntilTime(us(42));
        ir1033.Set(3);

        d.Timing.WaitUntilTime(us(65));
        ir1033.Set(0);

        d.Timing.WaitUntilTime(us(66));
        blue422.Update();

        blue422.SetFreq(0);
        d.Timing.WaitUntilTime(us(86));
        blue422.Update();

        blue422.SetFreq(branching_ratio_detuning);
        d.Timing.WaitUntilTime(us(87));
        blue422.Update();

        blue422.SetFreq(0);
        d.Timing.WaitUntilTime(us(107));
        blue422.Update();

        d.Timing.WaitUntilTime(us(108));
        ir1092.Enable();
        d.Timing.WaitUntilTime(us(131));
        ir1092.Disable();
        /*d.Timing.WaitUntilTime(us());
        ir1092.Enable();
        d.Timing.WaitUntilTime(us(123));
        ir1092.Disable();*/
    }

    DopplerCool(d,ir1092,blue422);
    blue422.SetFreq(F_Blue_End);
    blue422.SetAmp(A_Blue_End);
    blue422.Update();
    blue408.Disable();
    ir1033.Set(1);
}



