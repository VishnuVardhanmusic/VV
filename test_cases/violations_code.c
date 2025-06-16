#include <stdio.h>

int globalValue = 100;

void (*myFuncPtr)() = NULL;

void timerISR(void)
{
    printf("Inside ISR\n"); // blocking call in ISR
}

#define COMBINE(x, y) x##y // token pasting

void *getBuffer()
{
    return NULL; // void pointer usage
}

int main()
{
    int COMBINE(temp, Var) = 5;
    myFuncPtr = &timerISR;
    myFuncPtr();                // improper use of func pointer
    void *buffer = getBuffer(); // void pointer again
    return 0;
}
