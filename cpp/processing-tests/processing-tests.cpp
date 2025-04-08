#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/time.h"
#include <array>

#define ARRAY_SIZE 1000
#define MALLOC_AMT 800
#define FIB_SIZE 800
#define INPUT_PIN 14
#define OUTPUT_PIN 15
#define READY_PIN 16

bool is_sorted(volatile long arr[], unsigned int n)
{
    for (unsigned int i = 0; i < n - 1; i++)
    {
        if (arr[i] > arr[i + 1])
        {
            return false;
        }
    }
    return true;
}

int main()
{
    stdio_init_all();

    // Set the LED to be an output
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

    // Set the input pin
    gpio_init(INPUT_PIN);
    gpio_set_dir(INPUT_PIN, GPIO_IN);
    gpio_pull_down(INPUT_PIN);

    // Set the output pin
    gpio_init(OUTPUT_PIN);
    gpio_set_dir(OUTPUT_PIN, GPIO_OUT);
    gpio_put(OUTPUT_PIN, 0);

    // Set ready pin
    gpio_init(READY_PIN);
    gpio_set_dir(READY_PIN, GPIO_OUT);
    gpio_put(READY_PIN, 0);

    /* ############################################################################################################# */
    /* ####################################### CODE FOR TESTING STARTS HERE ######################################## */
    /* ############################################################################################################# */

    while(true)
    {

        // create a reversed array for the bubble sort test, which is the worst case
        volatile long numbers[ARRAY_SIZE];
        for (unsigned int i = 0; i < ARRAY_SIZE; i++)
        {
            numbers[i] = ARRAY_SIZE - i;
        }

        // allocate array for fibonacci test
        volatile double fib[FIB_SIZE] = {0.0};
        fib[0] = 0.0001;
        fib[1] = 1.0001;

        // indicate setup complete
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(500);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(500);
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(500);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);

        // indicate ready for tests
        gpio_put(READY_PIN, 1);
        gpio_put(OUTPUT_PIN, 0);

        /* #################### GPIO SPEED TEST ######################################################################## */

        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI
        gpio_put(OUTPUT_PIN, 1);          // indicate test complete
        while (gpio_get(INPUT_PIN) == 1); // wait for continue pin to go LOW
        gpio_put(OUTPUT_PIN, 0);          // indicate ready for next test

        /* #################### BUBBLE SORT PROCESSING TEST ############################################################ */

        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI

        //gpio_put(PICO_DEFAULT_LED_PIN, 1);

        for (unsigned int i = 0; i < ARRAY_SIZE; i++) // compute bubble sort
        {
            for (unsigned int j = 0; j < ARRAY_SIZE - i - 1; j++)
            {
                if (numbers[j] > numbers[j + 1])
                {
                    std::swap(numbers[j], numbers[j + 1]);
                }
            }
        }

        //gpio_put(PICO_DEFAULT_LED_PIN, 0);

        gpio_put(OUTPUT_PIN, 1); // indicate test complete

        // check if array is properly sorted
        if (is_sorted(numbers, ARRAY_SIZE) == false)
        {
            while (true) // halt program if improperly sorted
            {
                gpio_put(PICO_DEFAULT_LED_PIN, 1);
                sleep_ms(100);
                gpio_put(PICO_DEFAULT_LED_PIN, 0);
                sleep_ms(100);
            }
        }

        while (gpio_get(INPUT_PIN) == 1); // wait for continue pin to go LOW
        gpio_put(OUTPUT_PIN, 0);          // indicate ready for next test

        /* #################### HEAP ALLOC MEMORY TEST ############################################################ */

        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI

        //gpio_put(PICO_DEFAULT_LED_PIN, 1);

        for (int i = 0; i < MALLOC_AMT; i++)
        {
            unsigned char *ptr = new unsigned char[128];
            *ptr = 0;
            delete[] ptr; // Free immediately
        }

        //gpio_put(PICO_DEFAULT_LED_PIN, 0);

        gpio_put(OUTPUT_PIN, 1);          // indicate test complete
        while (gpio_get(INPUT_PIN) == 1); // wait for continue pin to go LOW
        gpio_put(OUTPUT_PIN, 0);          // indicate ready for next test

        /* #################### FIBONACCI PERFORMANCE TEST ############################################################ */

        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI

        //gpio_put(PICO_DEFAULT_LED_PIN, 1);

        for (int i = 2; i < FIB_SIZE; i++)
        {
            fib[i] = fib[i - 1] + fib[i - 2];
        }

        //gpio_put(PICO_DEFAULT_LED_PIN, 0);

        gpio_put(OUTPUT_PIN, 1); // indicate test complete
        while (gpio_get(INPUT_PIN) == 1); // wait for continue pin to go LOW
        gpio_put(OUTPUT_PIN, 0); // indicate ready for next test

        // indicate testing complete
        gpio_put(READY_PIN, 0);
        for (char i = 0; i < 5; i++)
        {
            gpio_put(PICO_DEFAULT_LED_PIN, 1);
            sleep_ms(100);
            gpio_put(PICO_DEFAULT_LED_PIN, 0);
            sleep_ms(100);
        }

        sleep_ms(1000);
    }

    /* ############################################################################################################# */
    /* ######################################## CODE FOR TESTING ENDS HERE ######################################### */
    /* ############################################################################################################# */

    return 0;
}
