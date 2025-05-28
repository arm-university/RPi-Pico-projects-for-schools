import picoexplorer as explorer
from machine import Pin
from utime import sleep

# Button and LED Setup
button_a = Pin(12, Pin.IN, Pin.PULL_UP)

led = Pin(0, Pin.OUT)  # Set up onboard LED pin

# Constants
ON = 1
OFF = 0
TIME_FOR_LIGHT = 20  # Number of seconds the LED will stay on

countdown = 0  # Countdown timer variable

while True:
    # Check if button A is pressed
    if button_a.value() == 0:  # Button is pressed (PULL_UP logic)
        countdown = TIME_FOR_LIGHT  # Start countdown
        led.value(ON)  # Turn LED on
    
    # Countdown logic
    if countdown > 0:
        countdown -= 1
        sleep(1)  # Wait for 1 second
    else:
        led.value(OFF)  # Turn LED off
        sleep(0.1)  # Short delay for loop stability


