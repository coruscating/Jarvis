// Ramsey lock, gives the center frequency for carrier and motional sidebands

#include "DDScon.h"
#include "HELPERS.h"
#include <math.h>

#define red         d.Ch1
#define blue        d.Ch0
#define ir1092      d.Ch2
#define ir1033      d.Digout

//Measurement frequencies
#define FCarrier       F_Red_Carrier
#define FRedSideband   F_Red_12_52_Red_Sideband
#define FBlueSideband  F_Red_12_52_Blue_Sideband
#define FRepump        F_Red_Repump


int main()
{
    DDScon d;
    d.Pmt0.Enable();
    Clear_mem(d);


    int plotindex=0;

    blue.Enable();
    ir1092.Enable();
    red.SetPhaseCoherent();
    red.SetAmp(A_Red);
    red.SetFreq(MHz(0));
    red.Update();
    red.Enable();

    int loop = 0;

    uint32_t realfreqCarrier       =FCarrier;
    uint32_t realfreqRedSideband   =FRedSideband;
    uint32_t realfreqRepump        =FRepump;
    uint32_t realfreqBlueSideband  =FBlueSideband;

    uint32_t a[4]               ={realfreqCarrier,realfreqRedSideband,realfreqBlueSideband,realfreqRepump};
    uint32_t TQubits[4]         ={T_Qubit_Pi,T_Qubit_Pi*2,T_Qubit_Pi*2,T_Polar_Pi};
    uint32_t b[4] = {1,1,1,0};
    for(loop = 0; loop < 1000; loop++){
        
        //Get frequencies
        a[loop%4]=RamseyLockIterate(d, red, ir1033, ir1092, blue, 20000, 3500, 51, a[loop%4] , TQubits[loop%4], T_Count, Count_Threshold, T_Repump,b[loop%4]);
     
        d.Plot.SetPoint(plotindex,((double)a[loop%4]/4294967.296)*1000000.0); plotindex++;
    
    }
    red.Disable();

}