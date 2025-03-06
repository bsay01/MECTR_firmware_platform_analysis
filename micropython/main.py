from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

while True:
    pin.toggle()
    sleep(0.5)
