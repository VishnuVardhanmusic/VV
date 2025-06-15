// test_bad.c

#include <stdio.h>
#include <stdint.h>

volatile int dataReady = 0;

void myISR()
{
    printf("Interrupt occurred!\n"); // ❌ Blocking call in ISR
    dataReady = 1;                   // ✅ Correctly using volatile
}

void configureInterrupts()
{
    // ❌ No interrupt disable before config
    registerISR(myISR); // Pseudo function
    enableInterrupts();
}

int main()
{
    while (1)
    {
        if (dataReady)
        {
            printf("Processing data...\n");
            dataReady = 0;
        }
    }
    return 0;
}
