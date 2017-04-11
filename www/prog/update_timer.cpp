#include "DDScon.h"
#define t d.Ch4.Out2
// CH0: 447 ns: amp
// 	507 ns: freq
//	112 ns: enable 
// CH1: 751 ns: amp, freq
//	351 ns: enable 
// CH2: 2.656 us: amp
// 	2.660 us: freq
//	208.6 ns: enable 
// CH3: 1.390 us: amp
// 	1.390 us: freq
// CH4: 26.8 us : volt
#define amp 50000


int main()

{
//        DDScon::Timing::WaitForSync();
//        DDScon::Timing::WaitForTime(ms(1000));
	DDScon d;
//	t.SetAmp(0*amp);
//	t.SetFreq(MHz(100));
	t.SetLevel(Volt(0));
	t.Update();
	d.Timing.WaitForTime(50);
	d.Digout.Set(3);
//	t.Disable();
//	t.Enable();
	d.Timing.WaitForTime(50);
	while(1) {
//		t.SetAmp(amp);
//		t.SetFreq(MHz(100));
		t.SetLevel(Volt(5));
		d.Timing.WaitForSync();

		d.Digout.Set(0);
//		t.Enable();
		t.Update();


		d.Timing.WaitForTime(ms(2000));
		d.Digout.Set(3);
//		t.SetAmp(0);
//		t.SetFreq(0);
		t.SetLevel(Volt(0));
		t.Update();
//		t.Disable();
	}
}
