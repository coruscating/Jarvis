#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout

#define lowamp 32000
#define highamp 40000


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
        //Doppler cool

        /*if(DopplerCool(d,ir1092,blue)==0){
            break;
        }*/
        DopplerCool(d,ir1092,blue);
    	//}
 
        d.Write(loop); // mark what loop we are on

        //Turn off doppler
        blue.SetAmp(0);
        blue.SetFreq(0);
        blue.Update();

        ir1092.SetAmp(A_1092_Det);
        ir1092.SetFreq(F_1092_Det);
        ir1092.Update();
        //Prepare in S state
        d.Timing.WaitForTime(us(20));
        ir1092.Disable();
        d.Timing.WaitForTime(us(5));

        
		//Prepare for measurement
		blue.SetAmp(lowamp);
		blue.SetFreq(F_Blue_Det);
		
		//Count photons until ion is shelved

		d.Timing.ZeroTime();
        d.Pmt0.SyncCorr().Clear();
		blue.Update(); 

        blue.SetFreq(MHz(0));
		d.Timing.WaitUntilTime(us(10));
        blue.Update();
        
        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(highamp);
        //Calibrate scattered counts   
        d.Timing.WaitUntilTime(us(12));
        blue.Update();

        blue.SetFreq(0);
        d.Timing.WaitUntilTime(us(22));
        blue.Update();

        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(lowamp);
        //Calibrate scattered counts   
        d.Timing.WaitUntilTime(us(24));
        blue.Update();

        blue.SetFreq(0);
        d.Timing.WaitUntilTime(us(34));
        blue.Update();        

        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(highamp);
        //Calibrate scattered counts   
        d.Timing.WaitUntilTime(us(36));
        blue.Update();

        blue.SetFreq(0);
        d.Timing.WaitUntilTime(us(46));
        blue.Update();   

		d.Timing.WaitUntilTime(us(48));
		ir1092.Enable();
        d.Timing.WaitUntilTime(us(60));
    }

    DopplerCool(d,ir1092,blue);
    blue.SetFreq(F_Blue_Det);
    blue.SetAmp(A_Blue_End);
    blue.Update();
    red.Disable();
    ir1033.Set(0);

}



