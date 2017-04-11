#include "DDScon.h"
#include "HELPERS.h"

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


#define loops 1000



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
	Clear_mem(d);
    float time=0;
    uint32_t a[400]={0};

    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();
    ir1033.Set(0);
for(time=0.1;time<30;time+=0.1){
    d.Write((int)(time*10));
    for( loop=0;loop<loops;loop++) {
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
		//Count photons
		d.Timing.ZeroTime();
		blue.Update(); 
		d.Timing.WaitUntilTime(us(time));
        a[(int)(10*time)]+=d.Pmt0.GetCount();    
        d.Pmt0.Clear();       

        blue.SetFreq(MHz(0));
        blue.Update();
		
        //re-pump
		d.Timing.ZeroTime();
		ir1092.Enable();
		d.Timing.WaitUntilTime(us(30));


        
    }
    d.Plot.SetPoint((int)(10*time),a[(int)(10*time)]);
}

    blue.SetFreq(F_Blue_Det);
    blue.Update();
    red.Disable();
    ir1033.Set(0);

}



