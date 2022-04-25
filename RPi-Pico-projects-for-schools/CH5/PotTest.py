import picoexplorer as explorer #Get access to the explorer board
from utime import sleep #Import just sleep from the utime library

buf = bytearray(explorer.get_width() * explorer.get_height() * 2) #display
#buffer (so you can initialise the explorer board)
explorer.init(buf) #Initialise the explorer board



while True:
 #Repeat forever
    pot = int(explorer.get_adc(0)*100) #Get the pot reading
    print(pot) #output the potentiometer reading
    sleep(0.1) #wait 1/10s before testing the pot again