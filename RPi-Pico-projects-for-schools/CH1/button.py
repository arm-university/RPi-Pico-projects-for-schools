import picoexplorer as explorer #Get access to the explorer board
from utime import sleep #Import just sleep from the utime library

buf = bytearray(explorer.get_width() * explorer.get_height() * 2) #display
#buffer (so you can initialise the explorer board)
explorer.init(buf) #Initialise the explorer board

ON = 1 #On equates to 1
OFF = 0 #Off equates to 0
LEDPIN = 0 #The GPIO pin the (external) LED is attached to
TIME_FOR_LIGHT = 20 #The number of seconds the light will stay on

led = machine.Pin(LEDPIN, machine.Pin.OUT) #Attach pin 25 (LEDPIN) to led variable
countdown = 0 #Keep track of how long the light should be on for

while True:
 #Repeat forever
    if explorer.is_pressed(explorer.BUTTON_A): #Check if the button is pressed. If so:
        countdown = TIME_FOR_LIGHT #Start the countdown
        led.value(ON) #Turn the LED on
        sleep(1) #Wait for 1 second 
    if countdown > 0: #While there is time left
        countdown = countdown - 1 #Decrement the time left
        sleep(1) #Sleep for one more second
    else:
        led.value(OFF) #Otherwise, turn off the LED
        sleep(0.1) #wait 1/10s before testing button again.