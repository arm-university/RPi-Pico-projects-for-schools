#STATES
START = 0
WAITING = 1
ENTERING = 2

state = START

while True:
    if state == START:
        #initialise anything needed
        #IF button pressed (Y)
        #THEN state = WAITING
    elif state == WAITING:
        #Increment time counter
        #Wait 1 second
        #IF time counter is 15 minutes
        #THEN state = ENTERING
    elif state == ENTERING:
        #Capture button presses
        #Capture time spent
        #Save to file
        #IF button pressed (Y)
        #THEN save to file and state = WAITING
        
        
        
