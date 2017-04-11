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
d.Pmt0.Enable();
d.Pmt0.ClearCorr();
d.Pmt0.SyncCorr().Clear();
}
