// 422 off lifetime

#include "DDScon.h"
#include "math.h"
#include "HELPERS.h"

// time for 422 to stay off
#define OFFTIME 2000
#define TRIALS 2


#define blue d.Ch0
#define ir1092 d.Ch2


#ifdef __LOG_SIZE
    #define PLOTSIZE __LOG_SIZE
#else
    #define PLOTSIZE 0x100
#endif

int main()
{
    DDScon d;
    d.Pmt0.Enable();
    uint32_t start_count=0;
    uint32_t b=0;
    d.Pmt0.Clear();
    d.Timing.WaitForTime(ms(100));
    start_count=d.Pmt0.GetCount();
    int count=0;
    uint32_t i=0;

    
    // reset plot
    for(count=0;count<4000;count++){
	d.Plot.SetPoint(count,0);
	}
    d.Plot.SetPoint(0, start_count);

    for (count=1;count<=TRIALS;count++){ 
        
        blue.SetAmp(0);
        blue.SetFreq(MHz(0));
        d.Timing.ZeroTime();
        blue.Update();
        d.Timing.WaitUntilTime(ms(OFFTIME));
        
        DopplerCool(d,ir1092,blue);

        blue.SetFreq(F_Blue_Det);
        blue.SetAmp(A_Blue_Det);
        blue.Update();
        d.Timing.WaitForTime(us(10));

        d.Pmt0.Clear();
        d.Timing.WaitForTime(ms(100));
        b=d.Pmt0.GetCount();
        d.Plot.SetPoint(count, b);
        
        if (b <= 1000){ // lost the ion
           break;
        }
        
        
    }       
    
    
    
}
