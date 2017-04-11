#include "DDScon.h"
#include "HELPERS.h"


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout
int main()
{
DDScon d;
//d.Ch0.SetPhaseCoherent();
uint32_t i=0;
uint32_t i2=us(10);
//while(1){
/*for(i=150;i<=250;i++){
	red.SetFreq(MHz(i));
	red.Update();
	d.Timing.WaitForTime(us(12));
}*/
/*	ir1092.Disable();
	d.Timing.WaitForTime(ms(1000));
	ir1092.Enable();
	d.Timing.WaitForTime(ms(1000));*/
		d.Pmt0.ClearCorr();



d.Pmt0.SyncCorr().Clear();
	blue.SetFreq(MHz(200));
	blue.Update();
	for(i=0;i<14;i++){
		d.Timing.WaitUntilTime(i2);
		i2+=us(10);
		blue.SetFreq(0);
		blue.Update();
	d.Timing.WaitUntilTime(i2);
	i2+=us(10);
	blue.SetFreq(MHz(200));
	blue.Update();
	
}
	blue.SetFreq(0);
	blue.Update();

}
//}
