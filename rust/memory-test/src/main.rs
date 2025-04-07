#![no_std]
#![no_main]

// Required for panic handler
use panic_probe as _;

// Import the RP-Pico board support package
use rp_pico::hal;
use rp_pico::hal::pac;
use core::arch::asm;

#[rp_pico::entry]
fn main() -> ! {
    // Get the peripherals
    let mut pac = pac::Peripherals::take().unwrap();
    let core = pac::CorePeripherals::take().unwrap();

    // Initialize the watchdog timer (needed for the clock)
    let mut watchdog = hal::Watchdog::new(pac.WATCHDOG);

    // Configure the clocks
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

    // Get the current stack pointer
    let stack_pointer: *const u32;
    unsafe {
        asm!("mov {}, sp", out(reg) stack_pointer);
    }

    // Get the current heap usage (if using alloc)
    // Note: This requires the alloc feature to be enabled

    // Memory layout information
    let ram_start = 0x20000000 as *const u32;
    let ram_end = unsafe { ram_start.add(264 * 1024 / 4) }; // RP2040 has 264KB RAM

    // Calculate available memory
    let stack_space = unsafe { stack_pointer.offset_from(ram_start) as usize * 4 };
    let total_ram = 264 * 1024; // 264KB
    let used_by_stack = total_ram - stack_space;
    let static_memory_usage = {
        extern "C" {
            static mut _sheap: u32;
            static mut _eheap: u32;
            static _sbss: u32;
            static _ebss: u32;
            static _sdata: u32;
            static _edata: u32;
        }

        unsafe {
            let bss_size = (&_ebss as *const u32 as usize) - (&_sbss as *const u32 as usize);
            let data_size = (&_edata as *const u32 as usize) - (&_sdata as *const u32 as usize);
            bss_size + data_size
        }
    };

    let available_for_heap = stack_space - static_memory_usage;

    // Print memory information (if you have a way to output, like semihosting or UART)
    // For actual output, you'd need to initialize a UART or other output method

    // In a real application, you might want to do something with this information
    // For now, we'll just loop forever
    loop {
        cortex_m::asm::nop();
    }
}
