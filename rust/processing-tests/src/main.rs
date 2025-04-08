#![no_std]
#![no_main]

extern crate alloc;

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

use embedded_alloc::LlffHeap as Heap;

#[global_allocator]
static HEAP: Heap = Heap::empty();

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
    let mut input_pin = pins.gpio14.into_floating_input(); // Set the input pin
    let mut output_pin = pins.gpio15.into_push_pull_output(); // Set the output pin
    let mut ready_pin = pins.gpio16.into_push_pull_output(); // Set ready pin

    /* ############################################################################################################# */
    /* ####################################### CODE FOR TESTING STARTS HERE ######################################## */
    /* ############################################################################################################# */

    loop {

        // create a reversed array for the bubble sort test, which is the worst case
        const ARRAY_SIZE: usize = 1000;
        let mut numbers: [i32; ARRAY_SIZE] = [0; ARRAY_SIZE];
        for i in 0..ARRAY_SIZE {
            numbers[i] = (ARRAY_SIZE - i) as i32;
        }

        // declare stuff for the heap alloc test
        const MALLOC_AMT: usize = 800;
        unsafe { HEAP.init(cortex_m_rt::heap_start() as usize, 1024 * 16) } // 16KB heap

        // allocate array for fibonacci test
        const FIB_SIZE: usize = 800;
        let mut fib = [0.0; FIB_SIZE];
        fib[0] = 0.0001;
        fib[1] = 1.0001;

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

        /* #################### BUBBLE SORT PROCESSING TEST ############################################################ */

        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI

        //led_pin.set_high().unwrap();

        let len = numbers.len(); // compute bubble sort
        for i in 0..len {
            for j in 0..len - i - 1 {
                if numbers[j] > numbers[j + 1] {
                    numbers.swap(j, j + 1);
                }
            }
        }

        //led_pin.set_low().unwrap();

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

        /* #################### HEAP ALLOC MEMORY TEST ############################################################ */

        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI

        //led_pin.set_high().unwrap();

        for _ in 0..MALLOC_AMT {
            let _x = alloc::boxed::Box::new([0u8; 128]);
            // Box is dropped (freed) at end of scope
        }

        //led_pin.set_low().unwrap();

        output_pin.set_high().unwrap(); // indicate test complete
        while input_pin.is_high().unwrap() {} // wait for continue pin to go LOW
        output_pin.set_low().unwrap(); // indicate ready for next test

        /* #################### FIBONACCI PERFORMANCE TEST ############################################################ */

        while input_pin.is_low().unwrap() {} // wait for continue pin to go HI

        //led_pin.set_high().unwrap();

        for i in 2..FIB_SIZE {
            fib[i] = fib[i-1] + fib[i-2];
        }

        //led_pin.set_low().unwrap();

        output_pin.set_high().unwrap(); // indicate test complete

        // to keep the compiler from optimizing the results out
        if fib[FIB_SIZE - 1] > 0.0 {
            led_pin.set_high().unwrap();
            delay.delay_ms(10);
            led_pin.set_low().unwrap();
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

fn is_sorted(arr: &[i32]) -> bool {
    for i in 0..arr.len() - 1 {
        if arr[i] > arr[i + 1] {
            return false;
        }
    }
    true
}

// End of file
