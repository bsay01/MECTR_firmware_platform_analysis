import time
from machine import Pin
import rp2

NUM_TESTS = 1
TEST_DELAY = 500

RUST_OUT_PIN = 0
RUST_IN_PIN = 1
CPP_OUT_PIN = 2
CPP_IN_PIN = 3
CIRCPY_OUT_PIN = 4
CIRCPY_IN_PIN = 5
MICROPY_OUT_PIN = 6
MICROPY_IN_PIN = 7
RUST_READY_PIN = 10
CPP_READY_PIN = 11
CIRCPY_READY_PIN = 12
MICROPY_READY_PIN = 13

# Onboard LED setup
led = Pin("LED", Pin.OUT)

def log_to_file(message):
    with open("output.txt", "a") as f:
        f.write(message)

# PIO program to wait for a rising edge and record time
@rp2.asm_pio()
def wait_for_high():
    # Wait for input pin to go high
    wait(1, pin, 0)

    # Push the current cycle count to the FIFO
    mov(isr, pins)
    push(noblock)

def measure_response_time(output_pin_num, input_pin_num):

    output_pin = Pin(output_pin_num, Pin.OUT)
    input_pin = Pin(input_pin_num, Pin.IN, Pin.PULL_DOWN)

    # Initialize PIO State Machine
    sm = rp2.StateMachine(
        0,                          # Use StateMachine 0
        wait_for_high,              # PIO program
        in_base=input_pin,          # Watch this input pin
        jmp_pin=input_pin           # Jump condition tied to input
    )

    # setup
    output_pin.low()
    time.sleep_us(50) # delay for safety

    # Start PIO SM
    sm.active(1)
    sm.restart()

    output_pin.high() # start test
    start_cpu = time.ticks_cpu()  # CPU cycle count at start of test

    # Wait for PIO to detect rising edge and return cycle count
    pio_cycles = sm.get()

    end_cpu = time.ticks_cpu() # CPU cycle count at end of test
    cpu_cycles = time.ticks_diff(end_cpu, start_cpu)

    cpu_time_us = cpu_cycles * 0.001  # CPU time in ms

    # cleanup
    output_pin.low()
    sm.active(0)

    return "{:0.4f}".format(cpu_time_us)

def flash_led(times, delay_ms=100):
    led.off()
    time.sleep_ms(100)
    for i in range(times):
        led.on()
        time.sleep_ms(delay_ms)
        led.off()
        time.sleep_ms(delay_ms)

######################### MAIN #########################

rust_out = Pin(RUST_OUT_PIN, Pin.OUT)
cpp_out = Pin(CPP_OUT_PIN, Pin.OUT)
circpy_out = Pin(CIRCPY_OUT_PIN, Pin.OUT)
micropy_out = Pin(MICROPY_OUT_PIN, Pin.OUT)

rust_out.low()
cpp_out.low()
circpy_out.low()
micropy_out.low()

rust_ready = Pin(RUST_READY_PIN, Pin.IN, Pin.PULL_DOWN)
cpp_ready = Pin(CPP_READY_PIN, Pin.IN, Pin.PULL_DOWN)
circpy_ready = Pin(CIRCPY_READY_PIN, Pin.IN, Pin.PULL_DOWN)
micropy_ready = Pin(MICROPY_READY_PIN, Pin.IN, Pin.PULL_DOWN)

rust_in = Pin(RUST_IN_PIN, Pin.IN)
cpp_in = Pin(CPP_IN_PIN, Pin.IN)
circpy_in = Pin(CIRCPY_IN_PIN, Pin.IN)
micropy_in = Pin(MICROPY_IN_PIN, Pin.IN)

flash_led(2)  # Startup indicator

"""
log_to_file("New test - prevented compiler optimization")
log_to_file("Rust [4] then C++ [4]")
log_to_file("GPIO, Bubble sort, Alloc, Fibonacci")
"""

for i in range(NUM_TESTS):

    print()

    led.on()
    while True:
        if rust_ready.value() and cpp_ready.value() and micropy_ready.value() and circpy_ready.value():
            break
    led.off()

    print("[" + str(i+1) + "]")

    ################ Rust ################

    print("Rust")

    time.sleep_ms(TEST_DELAY)
    while rust_in.value():
        pass
    print("    GPIO = ", end="")
    rust_io_str = measure_response_time(RUST_OUT_PIN, RUST_IN_PIN)
    print(rust_io_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while rust_in.value():
        pass
    print("    bubble sort = ", end="")
    rust_bs_str = measure_response_time(RUST_OUT_PIN, RUST_IN_PIN)
    print(rust_bs_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while rust_in.value():
        pass
    print("    memory allocation = ", end="")
    rust_ma_str = measure_response_time(RUST_OUT_PIN, RUST_IN_PIN)
    print(rust_ma_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while rust_in.value():
        pass
    print("    fibonacci = ", end="")
    rust_fb_str = measure_response_time(RUST_OUT_PIN, RUST_IN_PIN)
    print(rust_fb_str + " ms")

    ################ C++ ################

    print("C++")

    time.sleep_ms(TEST_DELAY)
    while cpp_in.value():
        pass
    print("    GPIO = ", end="")
    cpp_io_str = measure_response_time(CPP_OUT_PIN, CPP_IN_PIN)
    print(cpp_io_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while cpp_in.value():
        pass
    print("    bubble sort = ", end="")
    cpp_bs_str = measure_response_time(CPP_OUT_PIN, CPP_IN_PIN)
    print(cpp_bs_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while cpp_in.value():
        pass
    print("    memory allocation = ", end="")
    cpp_ma_str = measure_response_time(CPP_OUT_PIN, CPP_IN_PIN)
    print(cpp_ma_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while cpp_in.value():
        pass
    print("    fibonacci = ", end="")
    cpp_fb_str = measure_response_time(CPP_OUT_PIN, CPP_IN_PIN)
    print(cpp_fb_str + " ms")

    ################ CircuitPython ################

    print("CircuitPython")

    time.sleep_ms(TEST_DELAY)
    while circpy_in.value():
        pass
    print("    GPIO = ", end="")
    circpy_io_str = measure_response_time(CIRCPY_OUT_PIN, CIRCPY_IN_PIN)
    print(circpy_io_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while circpy_in.value():
        pass
    print("    bubble sort = ", end="")
    circpy_bs_str = measure_response_time(CIRCPY_OUT_PIN, CIRCPY_IN_PIN)
    print(circpy_bs_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while circpy_in.value():
        pass
    print("    memory allocation = ", end="")
    circpy_ma_str = measure_response_time(CIRCPY_OUT_PIN, CIRCPY_IN_PIN)
    print(circpy_ma_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while circpy_in.value():
        pass
    print("    fibonacci = ", end="")
    circpy_fb_str = measure_response_time(CIRCPY_OUT_PIN, CIRCPY_IN_PIN)
    print(circpy_fb_str + " ms")

    ################ MicroPython ################

    print("MicroPython")

    time.sleep_ms(TEST_DELAY)
    while micropy_in.value():
        pass
    print("    GPIO = ", end="")
    micropy_io_str = measure_response_time(MICROPY_OUT_PIN, MICROPY_IN_PIN)
    print(micropy_io_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while micropy_in.value():
        pass
    print("    bubble sort = ", end="")
    micropy_bs_str = measure_response_time(MICROPY_OUT_PIN, MICROPY_IN_PIN)
    print(micropy_bs_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while micropy_in.value():
        pass
    print("    memory allocation = ", end="")
    micropy_ma_str = measure_response_time(MICROPY_OUT_PIN, MICROPY_IN_PIN)
    print(micropy_ma_str + " ms")

    time.sleep_ms(TEST_DELAY)
    while micropy_in.value():
        pass
    print("    fibonacci = ", end="")
    micropy_fb_str = measure_response_time(MICROPY_OUT_PIN, MICROPY_IN_PIN)
    print(micropy_fb_str + " ms")

    file_str = ""

    #file_str += str(i+1) + ","

    file_str += rust_io_str + ","
    file_str += rust_bs_str + ","
    file_str += rust_ma_str + ","
    file_str += rust_fb_str + ","

    file_str += cpp_io_str + ","
    file_str += cpp_bs_str + ","
    file_str += cpp_ma_str + ","
    file_str += cpp_fb_str + ","

    file_str += circpy_io_str + ","
    file_str += circpy_bs_str + ","
    file_str += circpy_ma_str + ","
    file_str += circpy_fb_str + ","

    file_str += micropy_io_str + ","
    file_str += micropy_bs_str + ","
    file_str += micropy_ma_str + ","
    file_str += micropy_fb_str

    log_to_file(file_str + "\n")

    flash_led(3)  # Completion indicator
