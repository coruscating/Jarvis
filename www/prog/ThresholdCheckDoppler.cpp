#include "DDScon.h"
#include "HELPERS.h"

// finds threshold from counts returned from DopplerCool()

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout
#define loops 10000

int main()
{
    // Initialize:
    DDScon d;
    //red.Disable();
    int plotindex=0;
    uint32_t loop=0;
    d.Pmt0.Enable();
    uint32_t pmtcounts=0;
    int i=0;
    
    Clear_mem(d);
    blue.SetFreq(F_Blue_Det);
    blue.SetAmp(A_Blue_Det);
    blue.Update();
    blue.Enable();
    ir1092.Enable();


        for( loop=0;loop<loops;loop++) {
            d.Write(loop);
            pmtcounts=DopplerCool(d, ir1092, blue);
            d.Plot[pmtcounts]+=1;
        }
    blue.SetFreq(F_Blue_Det);
    blue.SetAmp(A_Blue_Det);
    blue.Update();
}



