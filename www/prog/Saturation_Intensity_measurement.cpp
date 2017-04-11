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
    

    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();
    ir1033.Set(0);

    d.Pmt0.ClearCorr();

    for( loop=0;loop<loops;loop++) {
        d.Write(loop); // mark what loop we are on
        
        //Doppler cool
        if(loops%100==0){
        	DopplerCool(d,ir1092,blue);
    	}

        //Turn off doppler
        blue.SetAmp(0);
        blue.SetFreq(MHz(0));
        blue.Update();

        //Prepare in S state
        d.Timing.WaitForTime(us(20));
        ir1092.Disable();

        
		//Prepare for measurement
		blue.SetAmp(A_Blue_Det);
		blue.SetFreq(F_Blue_Det);
		d.Pmt0.Clear();
		//Count photons until ion is shelved

		d.Timing.ZeroTime();
        d.Pmt0.SyncCorr();
		blue.Update(); 

		d.Timing.WaitUntilTime(us(20));

        d.Plot[0]+=d.Pmt0.GetCount();    
        d.Pmt0.Clear();       

        blue.SetFreq(MHz(0));

        //Calirbate scattered counts   
        d.Timing.WaitUntilTime(us(40));
        d.Plot[1]+=d.Pmt0.GetCount();
        blue.Update();

        d.Timing.ZeroTime();
        //Gap for Blue AOM to turn off.
		d.Timing.WaitUntilTime(us(10));
		//re-initialize count count photons for detection eff.
		d.Pmt0.Clear();
		d.Timing.ZeroTime();
		ir1092.Enable();
		d.Timing.WaitUntilTime(us(20));
		d.Plot[2]+=d.Pmt0.GetCount();

        d.Pmt0.Clear();
        d.Timing.WaitUntilTime(us(40));
        d.Plot[3]+=d.Pmt0.GetCount();

        
    }


    blue.SetFreq(F_Blue_Det);
    blue.Update();
    red.Disable();
    ir1033.Set(0);

}



