#include <stdio.h>
#include "DDScon.h"



void Clear_mem(void)
{
    DDScon d;
    int count;
    for(count=0;count<4096;count++){
	d.Plot.SetPoint(count,0);
	}
}
