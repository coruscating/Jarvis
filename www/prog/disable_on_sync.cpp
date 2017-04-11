#include "DDScon++.h"

int main() {
    DDScon d;
    d.Ch0.Enable();

    d.Timing.WaitForSync();
    d.Ch0.Disable();
}


