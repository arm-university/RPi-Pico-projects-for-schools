from huskylensPythonLibrary import HuskyLensLibrary
import time
try:
    from ppwhttp import *  # Try and get the ppwhttp library
    picowireless.init()  # Initialise the wireless board for the LED
except ImportError:  # If something goes wrong, output an error.
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")

# Initialize HuskyLens
husky = HuskyLensLibrary("I2C")  # Create the HuskyLens object as I2C

# Timing constants
UNKNOWN_TIMESPACE = 5  # How long an unknown has to be seen to trigger a warning
KNOWN_TIMESPACE = 5  # How long since a known face is seen to trigger a warning
LED_ON_TIMESPACE = 5  # How long the LED stays on for

# Timers
timeUnknown = None  # Time when an unknown face is seen
timeKnown = None  # Time when a known face is seen
LEDOnTime = None

# HTTP request configuration
HTTP_REQUEST_PORT = const(80)  # The (default) port used by a website
HTTP_REQUEST_HOST = "maker.ifttt.com"  # The site we want to connect to
HTTP_REQUEST_PATH = "/trigger/Unknown_Visitor/with/key/A_CONFUSING_STRING_THATS_PRIVATE"  # IFTTT webhook path

# Start Wi-Fi connection
start_wifi()  # Start the WiFi connection
set_dns(GOOGLE_DNS)  # Set DNS for lookups

# Handle the HTTP request
def handler(head, body):
    if "Congratulations" in body:
        set_led(0, 255, 0)  # Make the WiFi LED green
        print("IFTTT Sent OK")
    else:
        print("Error: {}".format(head))
        print("Body: {}".format(body))
        set_led(255, 0, 0)  # Make the WiFi LED red

# Deal with detected faces
def faceDetected(faceId):
    global timeKnown, timeUnknown, LEDOnTime

    if faceId == 0:  # Unknown face
        print("Unknown face detected!")
        if timeUnknown is None:
            timeUnknown = time.time()

        if timeUnknown is not None and (time.time() - timeUnknown) >= UNKNOWN_TIMESPACE:
            print("Unknown face seen for too long. Sending alert...")
            print(husky.command_request_screenshot())  # Attempt to capture a screenshot
            http_request(HTTP_REQUEST_HOST, HTTP_REQUEST_PORT, HTTP_REQUEST_HOST, HTTP_REQUEST_PATH, handler)
            timeUnknown = None  # Reset unknown timer
            LEDOnTime = time.time()  # Start LED timer

    elif faceId in [1, 2]:  # Known faces
        if faceId == 1:
            print("Hello, Stephen Fry!")
        elif faceId == 2:
            print("Hello, Hugh Laurie!")
        timeKnown = time.time()  # Update known face timer
        timeUnknown = None  # Reset unknown timer

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

        # Manage LED timer
        if LEDOnTime is not None and (time.time() - LEDOnTime) >= LED_ON_TIMESPACE:
            set_led(0, 0, 0)  # Turn the LED off
            LEDOnTime = None

    except Exception as e:
        print("Error during face detection:", e)

    time.sleep(1)  # Delay before the next loop
