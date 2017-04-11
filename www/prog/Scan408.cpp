#include "DDScon.h"
#include "HELPERS.h"

#define blue408 d.Ch1
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
    uint32_t freq = 0;
	uint32_t a=0;
	int count=0;
	int initialfreq=175;
	int plotindex = 0;
	uint32_t i=0;
	int freq2=0;
	int power=A_Blue_Det;
	uint32_t count_time = us(10);
	int loops=1000; //rich
	
    Clear_mem(d);
    blue.SetPhaseContinuous();
	blue.SetAmp(power);
	blue.Update();
    ir1033.Set(3);
    blue408.Enable();
        for( freq = MHz(initialfreq); freq <= MHz(185); freq = freq + kHz(500)) {
            //Doppler cool  
            for(count=0;count<loops;count++){      
                DopplerCool(d, ir1092, blue);
                blue.SetFreq(0);
                blue.Update();
                //Set measurement freq
                blue408.SetFreq(MHz(180));
                blue408.SetAmp(15000);
                blue408.Update();
                //Clear PMT and Count count_time
                d.Pmt0.Clear();
                d.Timing.WaitForTime(count_time); //rich
                a+=d.Pmt0.GetCount();
                //d.Write(count);

                //move back to cool-freq. to re-cool
                //blue.SetFreq(MHz(originalfreq));
                //blue.Update();
                //d.Timing.WaitForTime(ms(0.1));
            }
            //plot results
            d.Plot.SetPoint(plotindex,a);
            plotindex+=1;
            a=0;
       }
    //set end power and frequency
    blue.SetFreq(F_Blue_End);
    blue.SetAmp(A_Blue_End);
    blue.Update();
    blue408.Disable();
}
