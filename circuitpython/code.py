
import time
import board, busio, pwmio, digitalio, analogio, math

LED_pin = digitalio.DigitalInOut(board.LED)
LED_pin.direction = digitalio.Direction.OUTPUT

def sleep_and_flash(seconds):
    LED_pin.value = False
    while seconds != 0:
        LED_pin.value = True
        time.sleep(0.5)
        LED_pin.value = False
        time.sleep(0.5)
        seconds -= 1

while(1):
    sleep_and_flash(1)
