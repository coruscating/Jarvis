#include "DDScon.h"
#include "HELPERS.h"

#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout
#ifdef __LOG_SIZE
    #define PLOTSIZE __LOG_SIZE
#else
    #define PLOTSIZE 0x100
#endif

int main()
{
    // Initialize:
    DDScon d;
    d.Pmt0.Enable();

    int originalfreq = 210; //freq to recool to

	uint32_t a=0;
	int count=0;
	int initialfreq=100;
	int plotindex = 0;
	uint32_t i=0;
	uint32_t freq=0;
	int power=60000;
	uint32_t count_time = us(10);
	int loops=1000; //rich

	
    Clear_mem(d);
    blue.SetPhaseContinuous();
	blue.SetAmp(power);
	blue.Update();
    ir1092.Enable();


    for(freq=MHz(200);freq<=MHz(270);freq=freq+kHz(1000)){
blue.SetFreq(MHz(200));
blue.SetAmp(power);
        blue.Update();
        //blue.Enable();

        ir1092.SetFreq(freq);
        ir1092.SetAmp(65000);
        ir1092.Update();
        d.Timing.WaitForTime(ms(100));

        blue.SetFreq(freq);
        blue.SetAmp(50000);
        blue.Update();
        
        blue.Update();
        ir1092.SetFreq(MHz(200));
        ir1092.SetAmp(10000);
        ir1092.Update();
    }
       
    //set end power and frequency
    blue.SetFreq(MHz(205));
    blue.SetAmp(A_Blue_End);
    blue.Update();
}
