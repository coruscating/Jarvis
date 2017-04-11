#include "DDScon.h"
#include "HELPERS.h"


// resets to normal operating conditions


#define red d.Ch1
#define blue d.Ch0
#define ir1092 d.Ch2
#define ir1033 d.Digout


int main()
{
    DDScon d;

    blue.SetFreq(MHz(195));
    blue.SetAmp(47000);
    blue.SetPhaseContinuous();
    blue.Update();
    blue.Enable();
    ir1092.SetPhaseCoherent();
    ir1092.SetFreq(F_1092_Doppler);
    ir1092.SetAmp(A_1092_Doppler);
    ir1092.Update();
    ir1092.Enable();
    ir1033.Set(1);
    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.SetPhaseCoherent();
    red.Update();
    red.Enable();
}