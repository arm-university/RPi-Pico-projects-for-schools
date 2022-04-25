from huskylensPythonLibrary import HuskyLensLibrary
import time
try:
    from ppwhttp import * #Try and get the ppwhttp library
    picowireless.init() #Initialise the wireless board for the LED
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")


husky = HuskyLensLibrary("I2C") #Create the HuskyLens object as I2C 

UNKNOWN_TIMESPACE = 5 #How long an unknown has to be seen to trigger a warning
KNOWN_TIMESPACE = 5 #How long since a known face is seen to trigger a warning
LED_ON_TIMESPACE = 5 #How long the LED stays on for
timeUnknown = None #Time when an unknown face is seen
timeKnown = None #Time when a known face is seen
LEDOnTime = None

HTTP_REQUEST_PORT = const(80) #The (default) port used by a website
HTTP_REQUEST_HOST = "maker.ifttt.com" #The site we want to connect to
HTTP_REQUEST_PATH = "/trigger/Unknown_Visitor/with/key/A_CONFUSING_STRING_THATS_PRIVATE" #The path of the resource we want to access

start_wifi() #Start the WiFi connection
set_dns(GOOGLE_DNS) #When ready, set the DNS for lookups

#Handle the HTTP request
def handler(head, body):
    #IFTTT doesn't seem to return 200, but this works!
    if "Congratulations" in body:
        set_led(0, 255, 0) #Make the WiFi LED green
        print("IFTTT Sent ok")
    else:
        #Output the contents of the head and body for checking
        print("Error: {}".format(head))
        print("Body: {}".format(body))
        set_led(255, 0, 0) #Make the WiFi LED red

#Deal with detected faces
def faceDetected(faceId):
    global timeKnown,timeUnknown,LEDOnTime #Need to access these within the function
    if faceId == 0: #Face 0 is unknown
        print("Unknown!")
        if timeKnown == None:
            timeKnown = time.time() #First time we've seen an unknown face for a while!
        if timeKnown != None and (time.time() - timeKnown) >= KNOWN_TIMESPACE:
            #Seen a known face but not for a while, so it's probably not leaving frame
            print("Seen a known face but not for a while, so it's probably not leaving frame")
            print(husky.command_request_screenshot()) #This will produce an error
            timeKnown = None #Reset so we don't try and capture again
            #Send IFTTT
            http_request(HTTP_REQUEST_HOST,HTTP_REQUEST_PORT,HTTP_REQUEST_HOST,HTTP_REQUEST_PATH,handler)
            LEDOnTime = time.time() #So we can turn the green light off
        if timeUnknown != None and time.time() - timeUnknown  >= UNKNOWN_TIMESPACE:
            #Seen an unknown more than 5s ago, so probably not someone we know.
            print("Seen an unknown more than 5s ago, so probably not someone we know.")
            print(husky.command_request_screenshot()) #This will produce an error
            #Send IFTTT
            http_request(HTTP_REQUEST_HOST,HTTP_REQUEST_PORT,HTTP_REQUEST_HOST,HTTP_REQUEST_PATH,handler) 
            timeUnknown = None #Reset so we don't try and capture again
            LEDOnTime = time.time() #So we can turn the green light off  
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
  print(LEDOnTime)
  print(LED_ON_TIMESPACE)
  if LEDOnTime != None:
      print(LEDOnTime + LED_ON_TIMESPACE)
  print(time.time())
  print(LEDOnTime != None and (LEDOnTime + LED_ON_TIMESPACE) <= time.time())
  if LEDOnTime != None and (LEDOnTime + LED_ON_TIMESPACE) <= time.time():
      set_led(0,0,0) #Turn the LED off
