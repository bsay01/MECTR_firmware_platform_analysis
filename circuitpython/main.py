import time
import board
import digitalio
import array

ARRAY_SIZE = 1000
MALLOC_AMT = 800
FIB_SIZE = 800
INPUT_PIN = board.GP14
OUTPUT_PIN = board.GP15
READY_PIN = board.GP16

def is_sorted(arr, n):
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

# Set the LED to be an output
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set the input pin
input_pin = digitalio.DigitalInOut(INPUT_PIN)
input_pin.direction = digitalio.Direction.INPUT
input_pin.pull = digitalio.Pull.DOWN

# Set the output pin
output_pin = digitalio.DigitalInOut(OUTPUT_PIN)
output_pin.direction = digitalio.Direction.OUTPUT
output_pin.value = False

# Set ready pin
ready_pin = digitalio.DigitalInOut(READY_PIN)
ready_pin.direction = digitalio.Direction.OUTPUT
ready_pin.value = False

#############################################################################################################
####################################### CODE FOR TESTING STARTS HERE ########################################
#############################################################################################################

while True:

    # create a reversed array for the bubble sort test, which is the worst case
    numbers = array.array('i', [ARRAY_SIZE - i for i in range(ARRAY_SIZE)])

    # allocate array for fibonacci test
    fib = [0.0] * FIB_SIZE
    fib[0] = 0.0001
    fib[1] = 1.0001

    # indicate setup complete
    for i in range(2):
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)

    # indicate ready for tests
    ready_pin.value = True
    output_pin.value = False

    #################### GPIO SPEED TEST ####################################################################

    while not input_pin.value: # wait for continue pin to go HI
        pass
    output_pin.value = True    # indicate test complete
    while input_pin.value:     # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value = False   # indicate ready for next test

    #################### BUBBLE SORT PROCESSING TEST ########################################################

    while not input_pin.value: # wait for continue pin to go HI
        pass

    #led.value = True

    for i in range(ARRAY_SIZE): # compute bubble sort
        for j in range(ARRAY_SIZE - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

    #led.value = False

    output_pin.value = True # indicate test complete

    # check if array is properly sorted
    if not is_sorted(numbers, ARRAY_SIZE):
        while True:  # halt program if improperly sorted
            led.value = not led.value
            time.sleep(0.1)

    while input_pin.value:   # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value = False # indicate ready for next test

    #################### HEAP ALLOC MEMORY TEST #############################################################

    while not input_pin.value: # wait for continue pin to go HI
        pass

    #led.value = True

    for _ in range(MALLOC_AMT):
        lst = [i for i in range(128)]   # simulate memory allocation
        del lst

    #led.value = False

    output_pin.value = True  # indicate test complete
    while input_pin.value:   # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value = False # indicate ready for next test

    #################### FIBONACCI PERFORMANCE TEST #########################################################

    while not input_pin.value: # wait for continue pin to go HI
        pass

    #led.value = True

    for i in range(2, FIB_SIZE):
        fib[i] = fib[i - 1] + fib[i - 2]

    #led.value = False

    output_pin.value = True  # indicate test complete
    while input_pin.value:   # wait for continue pin to go LOW
        pass
    time.sleep(1)
    output_pin.value = False # indicate ready for next test

    # Indicate testing complete
    ready_pin.value = False

    # attempt to keep the interpreter from optimizing out the fib code
    st = ""
    for i in fib:
        st += str(i)
    print(st)

    for _ in range(5):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)

    time.sleep(1)

#############################################################################################################
######################################## CODE FOR TESTING ENDS HERE #########################################
#############################################################################################################
