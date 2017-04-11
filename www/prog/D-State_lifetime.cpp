#include "DDScon.h"
#include "HELPERS.h"

// rabi flops at set frequency


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


#define loops 100
#define qubit_transition F_Red_12_12
#define FRepump F_Red_n12_n12

#define MaxTime 2000
#define Timebin 10
int main()
{
    // Initialize:
    DDScon d;
    uint32_t a[2000]={0};
    uint32_t Dark_time=0;
    uint32_t ShelvedQ=0;
    //red.Disable();
    int plotindex=0;
    uint32_t loop=0;
    int count =0;
    d.Pmt0.Enable();
    uint32_t pmtcounts =0;
    int i=0;
	Clear_mem(d);

    int IonState=0;
    int times=0;
    int dpcounts=2000;

    
    

    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();
    ir1033.Set(0);
for(times=150;times<MaxTime;times=times+Timebin){
    if(dpcounts<1000){
        break;
    }
    dpcounts=0;
    for( loop=0;loop<loops;loop++) {
        IonState=0;
        //Doppler cool
        dpcounts+=DopplerCool(d,ir1092,blue);

        //Turn off doppler
        blue.SetAmp(0);
        blue.SetFreq(MHz(0));
        blue.Update();
        ir1092.Disable();
        Initialize(d,red,ir1033,ir1092,blue,5);
        
        //Pi pulse to D state
        red.SetFreq(qubit_transition);
        d.Timing.ZeroTime();
        red.Update();
        red.SetFreq(MHz(0));
        d.Timing.WaitUntilTime(T_Qubit_Pi);
        red.Update();
        d.Timing.ZeroTime();

        //Confirm Shelving
        IonState = StateDetection(d,ir1092,blue);
        //Turn off doppler
        blue.SetAmp(0);
        blue.SetFreq(MHz(0));
        blue.Update();
        ir1092.Disable();
        if(IonState==1){
            //Detect after time times 
            d.Timing.WaitUntilTime(ms(times));
            IonState=StateDetection(d,ir1092,blue);
            a[times]+=IonState;

        }
        else{
            loop=loop-1;
        }
        // enable 1033
        ir1033.Set(1);
        d.Timing.WaitForTime(T_Repump);
        ir1033.Set(0);
        d.Timing.WaitForTime(ms(1));
    }
    d.Plot.SetPoint(times/10-15,a[times]);
}
    red.Disable();
    ir1033.Set(0);

}



