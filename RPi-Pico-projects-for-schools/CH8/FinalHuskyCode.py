from huskylensPythonLibrary import HuskyLensLibrary
import time
from machine import Pin  # Import Pin for onboard LED control

# Initialize HuskyLens
husky = HuskyLensLibrary("I2C")  # Create the HuskyLens object using I2C

# Timing constants
UNKNOWN_TIMESPACE = 5  # How long an unknown face has to be seen to trigger a warning
KNOWN_TIMESPACE = 5  # How long since a known face is seen to reset
LED_ON_TIMESPACE = 5  # How long the onboard LED stays on

# Timers
timeUnknown = None  # Time when an unknown face is seen
timeKnown = None  # Time when a known face is seen
LEDOnTime = None  # Timer for how long the LED should stay on

# Initialize the onboard LED (Pico W's built-in LED)
led = Pin("LED", Pin.OUT)
led.off()  # Ensure LED is off at start

# Handle the HTTP request
def handler(head, body):
    if "Congratulations" in body:
        print("IFTTT Sent OK")
    else:
        print("Error:", head)
        print("Body:", body)

# Deal with detected faces
def faceDetected(faceId):
    global timeKnown, timeUnknown, LEDOnTime

    if faceId == 0:  # Unknown face detected
        print("Unknown face detected!")
        if timeUnknown is None:
            timeUnknown = time.time()

        if time.time() - timeUnknown >= UNKNOWN_TIMESPACE:
            print("Unknown face seen for too long. Sending alert...")
            print(husky.command_request_screenshot())  # Attempt to capture a screenshot
            
            # Turn on onboard LED for 5 seconds
            led.on()
            LEDOnTime = time.time()  # Store when LED was turned on

            # Send HTTP request to IFTTT
            http_request(HTTP_REQUEST_HOST, HTTP_REQUEST_PORT, HTTP_REQUEST_HOST, HTTP_REQUEST_PATH, handler)
            
            timeUnknown = None  # Reset unknown timer

    elif faceId in [1, 2]:  # Known faces
        if faceId == 1:
            print("Hello, Stephen Fry!")
        elif faceId == 2:
            print("Hello, Hugh Laurie!")
        
        timeKnown = time.time()  # Update known face timer
        timeUnknown = None  # Reset unknown face timer

    else:  # New or unprogrammed face
        print("New face detected! HuskyLens is learning new faces.")
        timeKnown = time.time()
        timeUnknown = None

# Knock test to confirm HuskyLens connection
print(husky.command_request_knock())  # Should print "Knock Received"

# Main loop
while True:
    try:
        result = husky.command_request()  # Get face details
        numFaces = len(result)  # Count detected faces

        if numFaces > 0:
            for face in result:
                if len(face) > 4:
                    faceId = face[4]  # Extract face ID
                    faceDetected(faceId)  # Handle detected face
                else:
                    print("Unexpected face data format:", face)
        else:
            print("No faces detected.")

        # Manage LED timer (Turn off after 5 seconds)
        if LEDOnTime is not None and (time.time() - LEDOnTime) >= LED_ON_TIMESPACE:
            led.off()  # Turn the LED off
            LEDOnTime = None  # Reset LED timer

    except Exception as e:
        print("Error during face detection:", e)

    time.sleep(1)  # Delay before the next loop


