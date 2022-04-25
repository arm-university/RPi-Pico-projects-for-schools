import picoexplorer as explorer #Get access to the explorer board
from utime import sleep #Import just sleep from the utime library

width = explorer.get_width() #Get access to the height
height = explorer.get_height() #and width to setup the buffer

display_buffer = bytearray(width * height * 2)  #Create the buffer for the screen
explorer.init(display_buffer) #Initialise the explorer (and screen)
explorer.set_audio_pin(0) #Connect the audio


def map_value(value, in_min, in_max, out_min, out_max):#Map the pot value
    return int((value - in_min) * (out_max-out_min) / (in_max-in_min)+out_min)


while True:
 #Repeat forever
    explorer.set_pen(255, 255, 255) #Set a white pen
    explorer.clear() #Clear the screen

    explorer.set_pen(0, 0, 0) #Set a black pen

    pot = int(explorer.get_adc(0)*100) #Get the pot reading
    print(pot, end=':') #output the potentiometer reading
    pot_mapped = map_value(pot,0,99,0,15) #Get the pot as 0-15
    print(pot_mapped) #Output for debugging
    explorer.text(str(pot_mapped)+' minutes',60,100,120) #Output for screen
    #Check buttons
    if explorer.is_pressed(explorer.BUTTON_A):
        print("A pressed")
    if explorer.is_pressed(explorer.BUTTON_B):
        print("B pressed")
    if explorer.is_pressed(explorer.BUTTON_X):
        print("X pressed")
    if explorer.is_pressed(explorer.BUTTON_Y):
        print("Y pressed")
    explorer.update() #Update the screen
    sleep(0.1) #wait 1/10s before testing button again