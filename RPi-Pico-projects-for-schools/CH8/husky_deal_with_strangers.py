from huskylensPythonLibrary import HuskyLensLibrary
import time

husky = HuskyLensLibrary("I2C") #Create the HuskyLens object as I2C 

UNKNOWN_TIMESPACE = 5 #How long an unknown has to be seen to trigger a warning
KNOWN_TIMESPACE = 5 #How long since a known face is seen to trigger a warning
timeUnknown = None #Time when an unknown face is seen
timeKnown = None #Time when a known face is seen

#Deal with detected faces
def faceDetected(faceId):
    global timeKnown,timeUnknown #Need to access these within the function
    if faceId == 0: #Face 0 is unknown
        print("Unknown!")
        if timeKnown == None:
            timeKnown = time.time() #First time we've seen an unknown face for a while!
        if timeKnown != None and (time.time() - timeKnown) >= KNOWN_TIMESPACE:
            #Seen a known face but not for a while, so it's probably not leaving frame
            print("Seen a known face but not for a while, so it's probably not leaving frame")
            print(husky.command_request_screenshot()) #This will produce an error
            timeKnown = None #Reset so we don't try and capture again
        if timeUnknown != None and time.time() - timeUnknown  >= UNKNOWN_TIMESPACE:
            #Seen an unknown more than 5s ago, so probably not someone we know.
            print("Seen an unknown more than 5s ago, so probably not someone we know.")
            print(husky.command_request_screenshot()) #This will produce an error
            timeUnknown = None #Reset so we don't try and capture again
        #print("Saved")
    elif faceId == 1: #Known face
        print("Stephen Fry")
        timeKnown = time.time() #Store when seen
        timeUnknown = None #Remove chance of triggering unknown
    elif faceId == 2: #Known face
        print("Hugh Laurie")
        timeKnown = time.time() #Store when seen
        timeUnknown = None #Remove chance of triggering unknown
    else: #A known face that we've not yet programmed!
        print("You've been learning new faces!")
        timeKnown = time.time() #Store when seen
        timeUnknown = None #Remove chance of triggering unknown


print(husky.command_request_knock()) #Knock knock - is it working?
while True: #Work forever
  result = husky.command_request() #Get the details of any faces
  #print(result)
  numFaces = len(result) #Check how many are identified
  if numFaces > 0: #If the list isn't empty, there are faces. 
      for face in result: #Go through each face
          faceId = face[4] #Get the face ID
          faceDetected(faceId) #And deal with it
  #print(time.time()) #Useful for debugging
  time.sleep(1) #Run once a second
