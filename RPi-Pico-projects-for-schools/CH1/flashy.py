import machine #Access to Pico 
import utime #sleep function

ON = 1 #On equates to 1
OFF = 0 #Off equates to 0
LEDPIN = 25 #The GPIO pin the LED is attached to
SLEEPTIME = 2 #The number of seconds' delay we want

led = machine.Pin(LEDPIN, machine.Pin.OUT) #Attach pin 25 (LEDPIN) to led variable

while True: #Repeat forever
    led.value(ON)  #LED on...
    utime.sleep(SLEEPTIME) #delay
    led.value(OFF) #LED off...
    utime.sleep(SLEEPTIME) #delay
    