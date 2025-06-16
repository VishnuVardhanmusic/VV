#include <stdio.h>

// ISR simulation
void timerISR(void)
{
    // Just setting a flag, no blocking calls
    int timerFlag = 1;
}

static int localCounter = 0;

typedef struct
{
    int id;
    char name[20];
} Device;

void processDevice(Device *d)
{
    // logic here
}

int main()
{
    Device d = {1, "Sensor"};
    processDevice(&d);
    return 0;
}
