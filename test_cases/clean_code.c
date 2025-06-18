#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "hardware_abstraction.h" // Abstracted hardware APIs

#define MAX_BUFFER_SIZE 128

// Safe function-like macro using inline
static inline int square(int x)
{
    return x * x;
}

// Layered design: hardware init separated
static void init_peripherals(void)
{
    if (!HAL_GPIO_InitSafe())
    {
        log_error("GPIO init failed");
    }
}

// Const and static used properly
static const int threshold = 10;
static char messageBuffer[MAX_BUFFER_SIZE];

// ISR shared variable marked volatile
volatile uint8_t irq_flag = 0;

// Minimal ISR with flag set, no blocking
void EXTI0_IRQHandler(void)
{
    irq_flag = 1;
    HAL_ClearEXTIFlag(); // Abstracted clearing
}

// Safe string copy
void copyMessage(const char *src)
{
    if (src && strlen(src) < MAX_BUFFER_SIZE)
    {
        strncpy(messageBuffer, src, MAX_BUFFER_SIZE - 1);
        messageBuffer[MAX_BUFFER_SIZE - 1] = '\0';
    }
}

// No recursion, iterative logic
int factorial(int n)
{
    if (n < 0)
        return -1;
    int result = 1;
    for (int i = 1; i <= n; ++i)
        result *= i;
    return result;
}

// Mutex protection for shared resource
void updateShared(int *shared, pthread_mutex_t *mutex, int value)
{
    if (shared && mutex)
    {
        pthread_mutex_lock(mutex);
        *shared = value;
        pthread_mutex_unlock(mutex);
    }
}

// RTOS-safe task
void rtosTask(void *params)
{
    while (1)
    {
        if (irq_flag)
        {
            irq_flag = 0;
            processInterrupt();
        }
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

int main(void)
{
    // Abstracted init logic
    init_peripherals();

    static int localCounter = 0; // Proper static usage

    char *buffer = (char *)safe_malloc(MAX_BUFFER_SIZE); // Safe malloc wrapper
    if (buffer != NULL)
    {
        strncpy(buffer, "Hello", MAX_BUFFER_SIZE - 1);
        buffer[MAX_BUFFER_SIZE - 1] = '\0';
        safe_free(buffer);
    }

    int arr[10];
    for (int i = 0; i < 10; ++i)
    {
        arr[i] = i;
    }

    if (xTaskCreate(rtosTask, "InterruptTask", 512, NULL, 2, NULL) != pdPASS)
    {
        log_error("Task creation failed");
    }

    int result = square(5);
    printf("Square: %d\n", result);

    TIM2->ARR = SYSTEM_CLOCK / 1000; // Formula, no hardcoded value

    return 0;
}
