import time #To enable the delay
import picoexplorer as explorer #Allow access to the Pico Explorer base

width = explorer.get_width() #Get access to the height
height = explorer.get_height() #and width to set up the buffer

display_buffer = bytearray(width * height * 2)  #Create the buffer for the screen
explorer.init(display_buffer) #Initialise the explorer (and screen)

#Create a bit of text for display
quote = '1925 IBM Manual: All parts should go together without forcing. '
quote += 'You must remember that the parts you are reassembling were disassembled by you. '
quote +='Therefore, if you can\'t get them together again, there must be a reason.'

while True: #Repeat forever
    explorer.set_pen(0, 0, 255) #Set a blue pen

    explorer.clear() #Clear the screen

    explorer.set_pen(255, 255, 255) #Set a white pen
    explorer.text(quote,20,20,200) #Write the text 20 in from the top left and wrap at 200
    explorer.update() #Update the screen
    time.sleep(0.01) #Sleep for 1/100 second before repeating the loop