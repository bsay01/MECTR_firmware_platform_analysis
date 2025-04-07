#![no_std]
#![no_main]

// for some reason this is needed for the linker?
use defmt_rtt as _;

use embedded_hal::digital::InputPin;
use embedded_hal::digital::OutputPin;

// The macro for our start-up function
use rp_pico::entry;

// Ensure we halt the program on panic (must be mentioned to link)
use panic_probe as _;

// Pull in any important traits
use rp_pico::hal::prelude::*;

// A shorter alias for the Peripheral Access Crate, which provides low-level register access
use rp_pico::hal::pac;

// A shorter alias for the Hardware Abstraction Layer, which provides higher-level drivers.
use rp_pico::hal;

// The `#[entry]` macro ensures the Cortex-M start-up code calls this function as soon as all global variables are initialised.
#[entry]
fn main() -> ! {
    let mut pac = pac::Peripherals::take().unwrap(); // grab singleton objects
    let core = pac::CorePeripherals::take().unwrap();
    let mut watchdog = hal::Watchdog::new(pac.WATCHDOG); // watchdog driver for clock setup

    // Configure the clocks
    // default is to generate a 125 MHz system clock
    let clocks = hal::clocks::init_clocks_and_plls(
        rp_pico::XOSC_CRYSTAL_FREQ,
        pac.XOSC,
        pac.CLOCKS,
        pac.PLL_SYS,
        pac.PLL_USB,
        &mut pac.RESETS,
        &mut watchdog,
    )
    .ok()
    .unwrap();

    let mut delay = cortex_m::delay::Delay::new(core.SYST, clocks.system_clock.freq().to_Hz()); // can delay for input time (ms)
    let sio = hal::Sio::new(pac.SIO);

    // Set the pins up according to their function on this particular board
    let pins = rp_pico::Pins::new(
        pac.IO_BANK0,
        pac.PADS_BANK0,
        sio.gpio_bank0,
        &mut pac.RESETS,
    );

    let mut led_pin = pins.led.into_push_pull_output(); // Set the LED to be an output
    let mut input_pin = pins.gpio0.into_floating_input(); // Set the input pin
    let mut output_pin = pins.gpio1.into_push_pull_output(); // Set the output pin
    let mut ready_pin = pins.gpio16.into_push_pull_output(); // Set ready pin

    /* ############################################################################################################# */
    /* ####################################### CODE FOR TESTING STARTS HERE ######################################## */
    /* ############################################################################################################# */

    loop {
        // set up for computing factorial
        //let n = 20000000; // adjust this value to modify computation time
        let n = 10000; // adjust this value to modify computation time
        let mut result = BigNumber::new();
        let keep_digit_count = 0;

        // create a reversed array for the bubble sort test, which is the worst case
        const ARRAY_SIZE: usize = 20000;
        let mut numbers: [i32; ARRAY_SIZE] = [0; ARRAY_SIZE];
        for i in 0..ARRAY_SIZE {
            numbers[i] = (ARRAY_SIZE - i) as i32;
        }

        // indicate setup complete
        led_pin.set_high().unwrap();
        delay.delay_ms(500);
        led_pin.set_low().unwrap();
        delay.delay_ms(500);
        led_pin.set_high().unwrap();
        delay.delay_ms(500);
        led_pin.set_low().unwrap();

        // indicate ready for tests
        ready_pin.set_high().unwrap();
        output_pin.set_low().unwrap();

        /* #################### GPIO SPEED TEST ######################################################################## */

        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI
        output_pin.set_high().unwrap(); // indicate test complete
        while input_pin.is_high().unwrap() {} // wait for continue pin to go LOW
        output_pin.set_low().unwrap(); // indicate ready for next test

        /* #################### FACTORIAL PROCESSING TEST ############################################################## */

        /*
        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI

        led_pin.set_high().unwrap();

        for i in 1..=n {
            // compute factorial
            result.multiply(i);
        }

        led_pin.set_low().unwrap();

        output_pin.set_high().unwrap(); // indicate test complete

        keep_digit_count = result.digit_count();
        if keep_digit_count > 0 {
            led_pin.set_high().unwrap();
            delay.delay_ms(10);
            led_pin.set_low().unwrap();
        }

        while input_pin.is_high().unwrap() {} // wait for continue pin to go LOW
        output_pin.set_low().unwrap(); // indicate ready for next test
        */

        /* #################### BUBBLE SORT PROCESSING TEST ############################################################ */

        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI

        led_pin.set_high().unwrap();

        let len = numbers.len(); // compute bubble sort
        for i in 0..len {
            for j in 0..len - i - 1 {
                if numbers[j] > numbers[j + 1] {
                    numbers.swap(j, j + 1);
                }
            }
        }

        led_pin.set_low().unwrap();

        output_pin.set_high().unwrap(); // indicate test complete

        if is_sorted(&numbers) == false {
            // check if array is properly sorted
            loop {
                // halt program if improperly sorted
                led_pin.set_high().unwrap();
                delay.delay_ms(100);
                led_pin.set_low().unwrap();
                delay.delay_ms(100);
            }
        }

        while input_pin.is_high().unwrap() {} // wait for continue pin to go LOW
        output_pin.set_low().unwrap(); // indicate ready for next test

        // indicate testing complete
        ready_pin.set_low().unwrap();
        for _ in 0..5 {
            led_pin.set_high().unwrap();
            delay.delay_ms(100);
            led_pin.set_low().unwrap();
            delay.delay_ms(100);
        }

        delay.delay_ms(1000);
    }

    /* ############################################################################################################# */
    /* ######################################## CODE FOR TESTING ENDS HERE ######################################### */
    /* ############################################################################################################# */
}

const MAX_DIGITS: usize = 35000;

// Big number implementation
struct BigNumber {
    digits: [u8; MAX_DIGITS], // Using u8 since each digit is 0-9
    length: usize,
}

impl BigNumber {
    const fn new() -> Self {
        BigNumber {
            digits: [0; MAX_DIGITS],
            length: 1,
        }
    }

    fn multiply(&mut self, n: u32) {
        let mut carry = 0;

        for i in 0..self.length {
            let product = u32::from(self.digits[i]) * n + carry;
            self.digits[i] = (product % 10) as u8;
            carry = product / 10;
        }

        while carry > 0 && self.length < MAX_DIGITS {
            self.digits[self.length] = (carry % 10) as u8;
            carry /= 10;
            self.length += 1;
        }
    }

    fn digit_count(&self) -> usize {
        self.length
    }
}

fn is_sorted(arr: &[i32]) -> bool {
    for i in 0..arr.len() - 1 {
        if arr[i] > arr[i + 1] {
            return false;
        }
    }
    true
}

// End of file
