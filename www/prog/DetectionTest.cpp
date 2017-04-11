#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define stateprep 0
#define runtime us(50.0)
#define timestep us(0.5)
#define loops 25000
#define qubit_transition F_Red_Carrier
#define stateprep_transition F_Red_n12_n12

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a=0;
    //red.Disable();
    int plotindex=0;
    uint32_t time=0;
    uint32_t loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
    
	Clear_mem(d);
    red.SetAmp(0);
    red.SetFreq(qubit_transition);
    red.Update();
    red.Enable();
    ir1033.Set(1);
    //red.SetAmp(20000);
    //red.Update();

    for( loop=0;loop<loops;loop++) {
        if(loop%100==0){
            DopplerCool(d, ir1092, blue);
        }
        if(loop%4000==0){
            Clear_mem(d);
        }
        d.Write(loop);
        //count

        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(A_Blue_Det);
        blue.Update();
        d.Pmt0.Clear();
        d.Timing.WaitForTime(us(500));
        /*d.Plot[d.Pmt0.GetCount()]+=1;*/
        d.Plot[loop%4000]=d.Pmt0.GetCount();

        blue.SetFreq(0);
        blue.Update();
        d.Timing.WaitForTime(us(20));
        
    }
    DopplerCool(d,ir1092,blue);
        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(A_Blue_Det);
        blue.Update();    
    red.Disable();
    ir1033.Set(0);

}



