from huskylensPythonLibrary import HuskyLensLibrary
import time

husky = HuskyLensLibrary("I2C") #Create the HuskyLens object as I2C 

#Deal with detected faces
def faceDetected(faceId):
    if faceId == 0: #Face 0 is unknown
        print("Unknown!")
    elif faceId == 1: #Known face
        print("Stephen Fry")
    elif faceId == 2: #Known face
        print("Hugh Laurie")
    else: #A known face that we've not yet programmed!
        print("You've been learning new faces!")

print(husky.command_request_knock()) #Knock knock - is it working?
while True: #Work forever
  result = husky.command_request() #Get the details of any faces
  #print(result)
  numFaces = len(result) #Check how many are identified
  if numFaces > 0: #If the list isn't empty, there are faces. 
      for face in result: #Go through each face
          faceId = face[4] #Get the face ID
          faceDetected(faceId) #And deal with it
  time.sleep(1) #Run once a second