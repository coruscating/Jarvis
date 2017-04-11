#include "DDScon.h"

int main()
{
	DDScon d;
	d.Pmt0.Enable();
    d.Timing.WaitForTime(ms(50));
    
    uint32_t photons=d.Pmt0.GetCount();
	d.Plot.SetPoint(20,photons);

/*
    DDScon pp;
       pp.Pmt3.Enable();                      // Start counting with photon counter 3
       pp.Timing.WaitUntilTime( ms(100) );    // Wait until 100 ms have passed since the beginning of program execution
       uint32_t photons = pp.Pmt3.GetCount(); // read the value of the counter at this instant, storing in as photons


	for(int i=0;i<100;i++) {
		d.Digout.Set(3);
		d.Digout.Set(0);
		d.Timing.WaitForTime(ms(50));
		if(i==25) {d.Pmt0.Clear();}
		if(i==60) {d.Pmt2.Enable();}
		if(i==75) {d.Pmt2.Disable();}
	}
	d.Pmt0.Read();
	uint32_t a = d.Pmt2.GetCount();
	uint32_t b = d.Pmt0.GetLastCount();
	d.Plot.SetPoint(10,a);*/
}
	

