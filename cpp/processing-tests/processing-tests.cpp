#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/time.h"
#include <array>

#define MAX_DIGITS 35000
#define ARRAY_SIZE 20000
#define INPUT_PIN 0
#define OUTPUT_PIN 1
#define READY_PIN 16

class BigNumber
{
private:
    std::array<unsigned char, MAX_DIGITS> digits;
    unsigned int length;

public:
    BigNumber() : digits{0}, length(1)
    {
        for (unsigned int i = 0; i < length; i++)
        {
            digits[i] = 0;
        }
        digits[0] = 1; // Initialize with 1
    }

    void multiply(unsigned long n)
    {
        unsigned long carry = 0;

        for (unsigned int i = 0; i < length; i++)
        {
            unsigned long product = digits[i] * n + carry;
            digits[i] = product % 10;
            carry = product / 10;
        }

        while (carry > 0 && length < MAX_DIGITS)
        {
            digits[length++] = carry % 10;
            carry /= 10;
        }
    }

    unsigned int digit_count() const
    {
        return length;
    }

    void print()
    {
        for (unsigned int i = 0; i < length; i++)
        {
            printf("%d", int(digits[i]));
        }
        printf("\n");
    }
};

bool is_sorted(const int32_t arr[], size_t n)
{
    for (size_t i = 0; i < n - 1; i++)
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

        // set up for computing factorial
        //const unsigned long n = 20000000; // adjust this value to modify computation time
        const unsigned long n = 10000; // adjust this value to modify computation time
        BigNumber result;
        volatile size_t keep_digit_count = 0;

        // create a reversed array for the bubble sort test, which is the worst case
        int32_t numbers[ARRAY_SIZE];
        for (size_t i = 0; i < ARRAY_SIZE; i++)
        {
            numbers[i] = ARRAY_SIZE - i;
        }

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

        /* #################### FACTORIAL PROCESSING TEST ############################################################## */

        /*
        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI

        gpio_put(PICO_DEFAULT_LED_PIN, 1);

        for (unsigned long i = 1; i <= n; i++)
        {
            result.multiply(i);
            if (i % 100 == 0)
            {
                result.print();
            }
        }

        gpio_put(PICO_DEFAULT_LED_PIN, 0);

        gpio_put(OUTPUT_PIN, 1);          // indicate test complete

        // force result usage so that the compiler doesn't optimize it out
        keep_digit_count = result.digit_count();
        if (keep_digit_count > 0)
        {
            gpio_put(PICO_DEFAULT_LED_PIN, 1);
            sleep_ms(10);
            gpio_put(PICO_DEFAULT_LED_PIN, 0);
        }

        while (gpio_get(INPUT_PIN) == 1); // wait for continue pin to go LOW
        gpio_put(OUTPUT_PIN, 0);          // indicate ready for next test
        */

        /* #################### BUBBLE SORT PROCESSING TEST ############################################################ */

        while (gpio_get(INPUT_PIN) == 0); // wait for continue pin to go HI

        gpio_put(PICO_DEFAULT_LED_PIN, 1);

        for (size_t i = 0; i < ARRAY_SIZE; i++) // compute bubble sort
        {
            for (size_t j = 0; j < ARRAY_SIZE - i - 1; j++)
            {
                if (numbers[j] > numbers[j + 1])
                {
                    std::swap(numbers[j], numbers[j + 1]);
                }
            }
        }

        gpio_put(PICO_DEFAULT_LED_PIN, 0);

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
