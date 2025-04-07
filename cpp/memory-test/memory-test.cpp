#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/watchdog.h"
#include "hardware/clocks.h"
#include "hardware/structs/watchdog.h"
#include "hardware/structs/clocks.h"

// Heap configuration
extern char __StackLimit; // Defined in linker script
extern char __HeapBase;   // Defined in linker script
extern char __HeapLimit;  // Defined in linker script

void report_memory() {
    // Get stack pointer
    register char* stack_ptr asm ("sp");

    // Calculate stack usage
    uint32_t stack_usage = (uint32_t)(0x20040000 - (uint32_t)stack_ptr);

    // Get heap information
    uint32_t heap_start = (uint32_t)&__HeapBase;
    uint32_t heap_end = (uint32_t)&__HeapLimit;
    uint32_t heap_size = heap_end - heap_start;

    // Get malloc stats (if available)
    extern char *__brkval;
    uint32_t heap_used = __brkval ? (uint32_t)__brkval - heap_start : 0;
    uint32_t heap_free = heap_size - heap_used;

    // Get RAM size (typically 264KB for RP2040)
    uint32_t ram_size = 264 * 1024;
    uint32_t total_used = stack_usage + heap_size;
    uint32_t ram_free = ram_size - total_used;

    // Print report
    printf("\n=== Memory Report ===\n");
    printf("RAM Total: %lu B\n", ram_size);
    printf("Stack Usage: %lu B\n", stack_usage);
    printf("Heap Total: %lu B\n", heap_size);
    printf("Heap Used: %lu B\n", heap_used);
    printf("Heap Free: %lu B\n", heap_free);
    printf("RAM Free: %lu B\n", ram_free);
    printf("===================\n");
}

int main() {
    // Initialize stdio (USB serial)
    stdio_init_all();

    sleep_ms(1000);

    // Blink LED to show activity
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

    while (true) {
        // Toggle LED
        gpio_put(PICO_DEFAULT_LED_PIN, !gpio_get(PICO_DEFAULT_LED_PIN));

        // Report memory usage
        report_memory();

        // Delay between reports
        sleep_ms(2000);
    }

    return 0;
}
