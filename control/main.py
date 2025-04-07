import time
from machine import Pin
import rp2

# Onboard LED setup
led = Pin("LED", Pin.OUT)

def log_to_file(message):
    """Appends a message to 'output.txt'."""
    with open("output.txt", "a") as f:
        f.write(message + "\n")

# PIO program to wait for a rising edge and record time
@rp2.asm_pio()
def wait_for_high():
    # Wait for input pin to go high
    wait(1, pin, 0)

    # Push the current cycle count to the FIFO
    mov(isr, pins)
    push(noblock)

def measure_response_time(output_pin_num, input_pin_num):
    """Measures time from output_pin high to input_pin high using PIO."""
    # Setup pins
    output_pin = Pin(output_pin_num, Pin.OUT)
    input_pin = Pin(input_pin_num, Pin.IN, Pin.PULL_DOWN)

    # Initialize PIO State Machine
    sm = rp2.StateMachine(
        0,                          # Use StateMachine 0
        wait_for_high,              # PIO program
        in_base=input_pin,          # Watch this input pin
        jmp_pin=input_pin           # Jump condition tied to input
    )

    # Start with output low
    output_pin.low()
    time.sleep_us(10)  # Debounce

    # Start PIO SM
    sm.active(1)
    sm.restart()

    # Set output high and record CPU start time
    output_pin.high()
    start_cpu = time.ticks_cpu()  # CPU cycle count

    # Wait for PIO to detect rising edge and return cycle count
    pio_cycles = sm.get()

    # Get CPU end time
    end_cpu = time.ticks_cpu()
    cpu_cycles = time.ticks_diff(end_cpu, start_cpu)

    # Convert cycles to microseconds (125MHz → 8ns per cycle)
    pio_time_us = pio_cycles * 0.008  # PIO time in µs
    cpu_time_us = cpu_cycles * 0.008  # CPU time in µs

    #print(f"GPIO{output_pin_num} to GPIO{input_pin_num}")
    #print(f"PIO Time: {pio_time_us:.3f} us")
    #print(f"CPU Time: {cpu_time_us:.3f} us")

    # Cleanup
    output_pin.low()
    sm.active(0)

    return cpu_time_us

def flash_led(times, delay_ms=100):
    """Flashes the onboard LED `times` times."""
    led.off()
    time.sleep_ms(100)
    for _ in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

######################### MAIN #########################

Rust_out = Pin(0, Pin.OUT)
Cpp_out = Pin(2, Pin.OUT)
circpy_out = Pin(4, Pin.OUT)
micropy_out = Pin(6, Pin.OUT)

Rust_out.low()
Cpp_out.low()
circpy_out.low()
micropy_out.low()

Rust_ready = Pin(10, Pin.IN, Pin.PULL_DOWN)
Cpp_ready = Pin(11, Pin.IN, Pin.PULL_DOWN)
circpy_ready = Pin(12, Pin.IN, Pin.PULL_DOWN)
micropy_ready = Pin(13, Pin.IN, Pin.PULL_DOWN)

Rust_in = Pin(1, Pin.IN)
Cpp_in = Pin(3, Pin.IN)
circpy_in = Pin(5, Pin.IN)
micropy_in = Pin(7, Pin.IN)

flash_led(2)  # Startup indicator

log_to_file("New test!")

for i in range(5):

    print()

    led.on()
    while True:
        if Rust_ready.value() and Cpp_ready.value():
            break
    led.off()

    #### Rust ####

    time.sleep_ms(1000)

    print("Rust GPIO... ", end="")
    Rust_io_str = "{:0.4f} ".format(measure_response_time(0, 1))
    print(Rust_io_str + "us")

    """
    time.sleep_ms(1000)

    print("Rust factorial... ", end="")
    Rust_fa_str = "{:0.4f} ".format(measure_response_time(0, 1))
    print(Rust_fa_str + "us")
    """

    time.sleep_ms(1000)

    print("Rust bubble sort... ", end="")
    Rust_bs_str = "{:0.4f} ".format(measure_response_time(0, 1))
    print(Rust_bs_str + " us")

    #### Cpp ####

    time.sleep_ms(1000)

    print("Cpp GPIO... ", end="")
    Cpp_io_str = "{:0.4f} ".format(measure_response_time(2, 3))
    print(Cpp_io_str + "us")

    """
    time.sleep_ms(1000)

    print("Cpp factorial... ", end="")
    Cpp_fa_str = "{:0.4f} ".format(measure_response_time(2, 3))
    print(Cpp_fa_str + "us")
    """

    time.sleep_ms(1000)

    print("Cpp bubble sort... ", end="")
    Cpp_bs_str = "{:0.4f} ".format(measure_response_time(2, 3))
    print(Cpp_bs_str + "us")

    log_to_file(Rust_io_str + Rust_bs_str + Cpp_io_str + Cpp_bs_str)

    flash_led(3)  # Completion indicator
