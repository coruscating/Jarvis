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
#define plotindex 42

int main()
{
    // Initialize:
    DDScon d;
    d.Pmt0.Enable();

    int originalfreq = 210; //freq to recool to
    uint32_t freq = MHz(200);
	uint32_t a=0;
	uint32_t count=0;
	int initialfreq=210;
	uint32_t i=0;
    int b=0;
	int freq2=0;
	int power=A_Blue_Det-15000;
	uint32_t count_time = us(2);
    uint32_t delay_time = us(1);
	
    //Clear_mem(d);
    blue.SetPhaseContinuous();
	blue.SetAmp(power);
	blue.Update();
    d.Pmt0.ClearCorr();

        //for( freq = MHz(initialfreq); freq >= MHz(170); freq = freq - kHz(1000)) {
            //Doppler cool  

            for(count=0;count<100000;count++){
                if (count>>4<<4==count){
                    DopplerCool(d, ir1092, blue);
                }

                blue.SetFreq(0);
                blue.Update();
                ir1092.Disable();
                ir1092.SetFreq(freq);
                ir1092.SetAmp(30000);
                ir1092.Update();

                d.Timing.WaitForTime(us(1));


                //Set measurement freq
                

                d.Timing.ZeroTime();
                d.Pmt0.SyncCorr().Clear();
                ir1092.Enable();

                //d.Timing.WaitUntilTime(delay_time);
                //d.Pmt0.Clear();

                /*for (i=us(0.1);i<=us(1);i+=us(0.1)){
                    d.Timing.WaitUntilTime(i);
                    d.Plot[plotindex]+=d.Pmt0.GetCount();
                    plotindex++;
                }*/

                d.Timing.WaitUntilTime(count_time);
                ir1092.Disable();
               
                d.Timing.WaitUntilTime(delay_time+count_time); //rich
                a=d.Pmt0.GetCount();
                d.Plot[plotindex]+=a;

                blue.SetFreq(F_Blue_Det);
                blue.SetAmp(A_Blue_Det);
                d.Timing.WaitForTime(us(1));
                blue.Update();
                blue.SetFreq(0);
                d.Timing.WaitForTime(us(20));
                blue.Update();

                //d.Write(count);

                //move back to cool-freq. to re-cool
                //blue.SetFreq(MHz(originalfreq));
                //blue.Update();
                //d.Timing.WaitForTime(ms(0.1));
            }
           
       //}
    //set end power and frequency
    blue.SetFreq(MHz(205));
    blue.SetAmp(A_Blue_End);
    blue.Update();
    ir1092.SetFreq(MHz(200));
    ir1092.SetAmp(A_1092_Doppler);
    ir1092.Update();
    ir1092.Enable();
    

}
