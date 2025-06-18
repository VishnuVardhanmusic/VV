#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "driver.h"

#define SQUARE(x) ((x) * (x)) + 5 // G029: multi-line macro
#define COMBINE(a, b) a##b        // G001: token pasting
#define MAX_BUFFER 256

void *getBuffer(); // G002: void pointer usage

int global_var; // G009: global variable

static void *ptr = NULL;

int recursive(int x)
{ // G021: recursive function
    if (x <= 0)
        return 0;
    return x + recursive(x - 1);
}

void ISR_Handler()
{                            // G023: logic inside ISR
    printf("ISR Triggered"); // G010, G017: printf in ISR
    malloc(20);              // G024: malloc in ISR
    EXTI->PR |= 0x01;        // G012: interrupt flag clearing
}

int main()
{
    __disable_irq(); // G011: disable interrupts

    char *buf = malloc(100); // G020, G022: malloc without null check
    strcpy(buf, "unsafe");   // G015: unsafe API
    int arr[10];
    arr[20] = 99; // G019: unbounded access

    void (*func)() = main; // G004: function pointer misuse

    HAL_GPIO_TogglePin(); // G007, G018: HAL call without check
    LL_ADC_Enable();      // G007 again

    while (1)
        ; // G006, G033: busy loop

    vTaskDelay(100);                               // G014: blocking call in RTOS
    xTaskCreate(NULL, "task", 128, NULL, 1, NULL); // G016: small task

    UART_Write("Debug"); // G017: Debug UART

    int result = (int *)ptr; // G003: pointer cast
    volatile int flag = 0;   // G013: Volatile okay
    flag = 1;                // G025: shared variable no lock

    pthread_mutex_lock(&lock); // G026: possible deadlock

#ifdef __GNUC__
    __asm__("NOP"); // G031, G032: compiler-specific
#endif

    TIM2->ARR = 48000; // G034: hardcoded timer config

    return 0;
}
