#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


int main()
{
    // Initialize:
    DDScon d;
    //red.Disable();
    int plotindex=0;
    uint32_t loops=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts=0;
    int i=0;
    
    Clear_mem(d);
    blue.SetFreq(F_Blue_Det);
    blue.SetAmp(A_Blue_Det);
    blue.Update();
    blue.Enable();
    ir1092.Enable();

    ir1033.Set(1);
    red.SetAmp(13000);
    red.SetFreq(MHz(180));
    red.Update();
    red.Enable();
    
        for( loops=0;loops<100000;loops++) {
            //count
            d.Pmt0.Clear();
            d.Timing.WaitForTime(T_Count);
            pmtcounts=d.Pmt0.GetCount();

            d.Plot[pmtcounts]+=1;
        }

}



