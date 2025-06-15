// test_good.c

#include <stdint.h>

volatile int dataReady = 0;

void myISR()
{
    dataReady = 1; // ✅ No blocking calls, using volatile
}

void configureInterrupts()
{
    disableInterrupts(); // ✅ Interrupts disabled before config
    registerISR(myISR);  // Pseudo function
    enableInterrupts();  // Re-enable after config
}

int main()
{
    while (1)
    {
        if (dataReady)
        {
            processData(); // ✅ Abstracted processing
            dataReady = 0;
        }
    }
    return 0;
}
