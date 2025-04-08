import time
from machine import Pin

ARRAY_SIZE = 1000
MALLOC_AMT = 800
FIB_SIZE = 800
INPUT_PIN = 14
OUTPUT_PIN = 15
READY_PIN = 16

def is_sorted(arr, n):
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

# Set the LED to be an output
led = Pin("LED", Pin.OUT)

# Set the input pin
input_pin = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)

# Set the output pin
output_pin = Pin(OUTPUT_PIN, Pin.OUT)
output_pin.value(0)

# Set ready pin
ready_pin = Pin(READY_PIN, Pin.OUT)
ready_pin.value(0)

#############################################################################################################
####################################### CODE FOR TESTING STARTS HERE ########################################
#############################################################################################################

while True:

    # create a reversed array for the bubble sort test, which is the worst case
    numbers = [ARRAY_SIZE - i for i in range(ARRAY_SIZE)]

    # allocate array for fibonacci test
    fib = [0.0] * FIB_SIZE
    fib[0] = 0.0001
    fib[1] = 1.0001

    # indicate setup complete
    for _ in range(2):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)

    # indicate ready for tests
    ready_pin.value(1)
    output_pin.value(0)

    #################### GPIO SPEED TEST ####################################################################

    while not input_pin.value(): # wait for continue pin to go HI
        pass
    output_pin.value(1)          # indicate test complete
    while input_pin.value():     # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value(0)          # indicate ready for next test

    #################### BUBBLE SORT PROCESSING TEST ########################################################

    while not input_pin.value(): # wait for continue pin to go HI
        pass

    #led.value(1)

    for i in range(ARRAY_SIZE): # compute bubble sort
        for j in range(ARRAY_SIZE - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

    #led.value(0)

    output_pin.value(1) # indicate test complete

    # check if array is properly sorted
    if not is_sorted(numbers, ARRAY_SIZE):
        while True:  # halt program if improperly sorted
            led.value(not led.value())
            time.sleep(0.1)

    while input_pin.value(): # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value(0)      # indicate ready for next test

    #################### HEAP ALLOC MEMORY TEST #############################################################

    while not input_pin.value(): # wait for continue pin to go HI
        pass

    #led.value(1)

    for _ in range(MALLOC_AMT):
        lst = [i for i in range(128)]   # simulate memory allocation
        del lst

    #led.value(0)

    output_pin.value(1)      # indicate test complete
    while input_pin.value(): # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value(0)      # indicate ready for next test

    #################### FIBONACCI PERFORMANCE TEST #########################################################

    while not input_pin.value(): # wait for continue pin to go HI
        pass

    #led.value(1)

    for i in range(2, FIB_SIZE):
        fib[i] = fib[i - 1] + fib[i - 2]

    #led.value(0)

    output_pin.value(1)      # indicate test complete
    while input_pin.value(): # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value(0)      # indicate ready for next test

    # Indicate testing complete
    ready_pin.value(0)

    # attempt to keep the interpreter from optimizing out the bubble sort code
    n = 0
    for i in numbers:
        n += i
    print(n)

    # attempt to keep the interpreter from optimizing out the fib code
    n = 0
    for i in fib:
        st += i
    print(n)

    for _ in range(5):
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.1)

    time.sleep(1)

#############################################################################################################
######################################## CODE FOR TESTING ENDS HERE #########################################
#############################################################################################################
