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
    uint32_t freq = 0;
	uint32_t a=0;
	int count=0;
	int initialfreq=180;
	int plotindex = 2;
	uint32_t i=0;
	int freq2=0;
	int power=A_Blue_Det;
	uint32_t count_time = us(10);
	int loops=50; //rich
	
    Clear_mem(d);
    blue.SetPhaseContinuous();
	blue.SetAmp(power);
	blue.Update();
    d.Plot.SetPoint(0,20);
    d.Plot.SetPoint(1,90);
    while(1){
        for( freq = MHz(initialfreq); freq <= MHz(230); freq = freq + kHz(500)) {
            //Doppler cool  
            for(count=0;count<loops;count++){      
                if (count%4==0){
                    DopplerCool(d, ir1092, blue);
                }

                //Set measurement freq
                blue.SetFreq(freq);
                blue.SetAmp(power);
                blue.Update();
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
       plotindex=2;
    }
    //set end power and frequency
    blue.SetFreq(MHz(205));
    blue.SetAmp(A_Blue_End);
    blue.Update();
}
