import picoexplorer as explorer #Get access to the explorer board
from utime import sleep #Import just sleep from the utime library

buf = bytearray(explorer.get_width() * explorer.get_height() * 2) #display
#buffer (so you can initialise the explorer board)
explorer.init(buf) #Initialise the explorer board

def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max-out_min) / (in_max-in_min)+out_min)


while True:
 #Repeat forever
    pot = int(explorer.get_adc(0)*100) #Get the pot reading
    print(pot, end=':') #output the potentiometer reading
    print(map_value(pot,0,99,0,15))
    if explorer.is_pressed(explorer.BUTTON_A):
        print("A pressed")
    if explorer.is_pressed(explorer.BUTTON_B):
        print("B pressed")
    if explorer.is_pressed(explorer.BUTTON_X):
        print("X pressed")
    if explorer.is_pressed(explorer.BUTTON_Y):
        print("Y pressed")
    sleep(0.1) #wait 1/10s before testing button again