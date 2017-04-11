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
    uint32_t a[100];
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
    uint32_t tblue =us(10);
    uint32_t tgap = tblue+us(50);
    uint32_t tIR = tgap+us(10);
    for (i=0;i<100;i++){
        a[i]=0;
    }


        for( loops=0;loops<50000;loops++) {
            if(loops%100==0){
            DopplerCool(d, ir1092, blue);
            }
            blue.SetAmp(A_Blue_Det);
            blue.SetFreq(MHz(0));
            blue.Update();
            ir1092.Disable();
            ir1033.Set(0);

            //Turn blue on, set timer to zero
            blue.SetFreq(MHz(205));
            d.Timing.ZeroTime();
            blue.Update(); 
            
            //Turn off blue
            blue.SetFreq(MHz(0));
            d.Timing.WaitUntilTime(tblue);
            blue.Update();
            //Give time for blue to turn off
            d.Timing.WaitUntilTime(tgap);
            //Turn on 1092 for us(10), and count
            d.Pmt0.Clear();
            ir1092.Enable();
            d.Timing.WaitUntilTime(tIR);
            pmtcounts=d.Pmt0.GetCount();

            a[pmtcounts]+=1;
        }

    for(count=0;count<10;count++){
        d.Plot.SetPoint(count,a[count]);
    }
    blue.SetAmp(A_Blue_Det);
    blue.SetFreq(F_Blue_Det);
    blue.Update(); 
}



