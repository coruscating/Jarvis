#include "DDScon.h"
#include "HELPERS.h"

// rabi flops at set frequency


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define stateprep 0
#define runtime us(50.0)
#define timestep us(0.5)
#define loops 100096
#define qubit_transition F_Red_12_52
#define stateprep_transition F_Red_n12_32

int main()
{
    // Initialize:
    DDScon d;
    uint32_t a[2000];
    uint32_t Dark_time=0;
    uint32_t ShelvedQ=0;
    //red.Disable();
    int plotindex=0;
    uint32_t time=0;
    uint32_t loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
	Clear_mem(d);
    
    for(count=0; count<2001;count++){
        a[count]=0;
    }
    
    


    red.SetAmp(3000);
    red.SetFreq(qubit_transition);
    red.Update();
    red.Enable();
    ir1033.Set(0);

    for( loop=0;loop<loops;loop++) {        
        //count
        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(A_Blue_Det);
        d.Pmt0.Clear();
        d.Timing.WaitForTime(T_Count);
        pmtcounts=d.Pmt0.GetCount();
        
        if(pmtcounts<=Count_Threshold){
            Dark_time+=1;
            ShelvedQ=1;
        }
        
        if(Dark_time>2000){
            red.Disable();
            ir1033.Set(0);
            return(0);
        }
        
        if(pmtcounts>=Count_Threshold && ShelvedQ==1){
            a[Dark_time]+=1;
            d.Plot.SetPoint(Dark_time,a[Dark_time]);
            ShelvedQ=0;
            Dark_time=0;
        }
        
        if (loop%50==0){
            red.Disable();
            DopplerCool(d, ir1092, blue);
            red.Enable();
        }
    }

    red.Disable();
    ir1033.Set(0);

}



