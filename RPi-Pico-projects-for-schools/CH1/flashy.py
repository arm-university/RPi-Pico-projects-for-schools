from machine import Pin
from utime import sleep

# Constants
ON = 1
OFF = 0
SLEEPTIME = 2  # Number of seconds delay

# set up the LED PIN
led = Pin("LED", Pin.OUT)  # Set up onboard LED pin


while True:
    led.value(ON)
    sleep(SLEEPTIME)
    led.value(OFF)
    sleep(SLEEPTIME)
    
    
    
    
