import picoexplorer as explorer #Get access to the explorer board
from utime import sleep #Import just sleep from the utime library

width = explorer.get_width() #Get access to the height
height = explorer.get_height() #and width to setup the buffer

display_buffer = bytearray(width * height * 2)  #Create the buffer for the screen
explorer.init(display_buffer) #Initialise the explorer (and screen)
explorer.set_audio_pin(0) #Connect the audio

def map_value(value, in_min, in_max, out_min, out_max):#Map the pot value
    return int((value - in_min) * (out_max-out_min) / (in_max-in_min)+out_min)

#STATES
START = 0
WAITING = 1
ENTERING = 2

FILENAME = "socialmedia.csv" #The filename to store data in

period = 0 #Incrementing period to keep track of when in the day the recording was made

MAXCOUNTER = 60*15 #wait 15m – change this number to wait a shorter period for testing

state = START #begin in START state

#List of social media and whether they've been checked or not
social_media = [['YouTube',False,20,20],['Facebook',False,20,200],['Pinterest',False,140,20]]


while True: #Repeat forever
    if state == START:
        counter = 0 #Time counter
        explorer.set_pen(255, 255, 255) #Set a white pen
        explorer.clear() #Clear the screen
        explorer.set_pen(0, 0, 0) #Set a black pen
        explorer.text('Press Y to start',60,100,120) #Output for screen
        if explorer.is_pressed(explorer.BUTTON_Y): #Y pressed
            state = WAITING
        f = open(FILENAME, "w") #Open the file for writing and add headings
        fileString = 'period'+','+social_media[0][0]+','+social_media[1][0]+','+social_media[2][0]
        fileString = fileString +','+'time_spent'
        fileString = fileString +'\n' #Add a new line (like pressing ENTER)
        f.write(fileString) #Write the data to file
        f.close() #Close the file
        sleep(0.2) #Wait...
    elif state == WAITING:
        explorer.set_pen(255, 255, 255) #Set a white pen
        explorer.clear() #Clear the screen
        explorer.set_pen(0, 0, 0) #Set a black pen
        explorer.text('Waiting...',60,100,120) #Output for screen
        explorer.text(str(MAXCOUNTER-counter)+' s',60,120,120) #Output for screen
        counter += 1 #Increment time counter
        sleep(1) #Wait 1 second
        if counter == MAXCOUNTER: #IF time counter is 15 minutes
            counter = 0 #Reset counter
            state = ENTERING #Change state
    elif state == ENTERING:
        explorer.set_pen(255, 255, 255) #Set a white pen
        explorer.clear() #Clear the screen
        for sm in range(3):
            if social_media[sm][1] == False:
                explorer.set_pen(255, 0, 0) #Set a red pen
            else:
                explorer.set_pen(0, 255, 0) #Set a green pen
            #Output for screen
            explorer.text(social_media[sm][0],social_media[sm][2],social_media[sm][3],120) 
        #Capture button presses
        if explorer.is_pressed(explorer.BUTTON_A): #A pressed
            social_media[0][1] = not social_media[0][1] #Invert
        if explorer.is_pressed(explorer.BUTTON_B): #B pressed
            social_media[1][1] = not social_media[1][1] #Invert
        if explorer.is_pressed(explorer.BUTTON_X): #X pressed
            social_media[2][1] = not social_media[2][1] #Invert
        sleep(0.2)

        #Capture time spent
        pot = int(explorer.get_adc(0)*100) #Get the pot reading
        pot_mapped = map_value(pot,0,99,0,15) #Get the pot as 0-15
        explorer.set_pen(0, 0, 255) #Set a blue pen
        explorer.text(str(pot_mapped)+' minutes',60,100,120) #Output for screen
        
        #Confirmation
        explorer.text("Confirm",140,200,120)
        if explorer.is_pressed(explorer.BUTTON_Y):#IF button pressed (Y)
            period += 1 #Increment period
            f = open(FILENAME, "a") #Open the file for appending
            fileString = str(period)+','+str(social_media[0][1])+','+str(social_media[1][1])+','+str(social_media[2][1])
            fileString = fileString +','+str(pot_mapped)
            fileString = fileString +'\n' #Add a new line (like pressing ENTER)
            f.write(fileString) #Write the data to file
            f.close() #Close the file
            state=WAITING
    explorer.update() #Update the screen
    print(state)

