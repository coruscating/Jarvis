#include "DDScon.h"
#include "HELPERS.h"

// rabi flops at set frequency


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

        d.Write(loop+1); // mark what loop we are on

        //Turn off doppler
        blue.Disable();
        d.Timing.WaitForTime(us(2));

        d.Pmt0.SyncCorr();
        //d.Timing.WaitForTime(us(100));
        //blue.Enable();
        d.Timing.WaitForTime(us(100));

    }


}



