from huskylensPythonLibrary import HuskyLensLibrary
import time

# Initialize HuskyLens
husky = HuskyLensLibrary("I2C")  # Create the HuskyLens object using I2C communication

# Timer thresholds in seconds
UNKNOWN_TIMESPACE = 5  # Time to wait before confirming an unknown face
KNOWN_TIMESPACE = 5    # Time to wait before confirming a known face

# Initialize timers
timeUnknown = None  # Timestamp for when an unknown face is first detected
timeKnown = None    # Timestamp for when a known face is last detected

# Function to handle detected faces
def handle_detected_face(faceId):
    """
    Handles actions based on the face ID detected by HuskyLens.
    :param faceId: ID of the detected face
    """
    global timeUnknown, timeKnown

    if faceId == 0:  # Face ID 0 indicates an unknown face
        print("Unknown face detected!")
        if timeUnknown is None:
            timeUnknown = time.time()  # Record the first time an unknown face is detected
        if timeUnknown and (time.time() - timeUnknown) >= UNKNOWN_TIMESPACE:
            print("Unknown face confirmed after 5 seconds!")
            timeUnknown = None  # Reset the timer
    elif faceId in [1, 2]:  # Face IDs 1 and 2 correspond to known faces
        if faceId == 1:
            print("Hello, Stephen Fry!")
        elif faceId == 2:
            print("Hello, Hugh Laurie!")
        timeKnown = time.time()  # Update the known face timer
        timeUnknown = None      # Reset the unknown timer
    else:  # New or unprogrammed face IDs
        print("New face detected! HuskyLens is learning new faces.")
        timeKnown = time.time()  # Treat new face as a known face temporarily

# Main loop for face detection
while True:
    try:
        # Request face data from HuskyLens
        result = husky.command_request()  # Retrieve details of detected faces
        print("Face Data:", result)  # Print raw data for debugging
        
        # Check if faces are detected
        if result and isinstance(result, list):
            for face in result:
                # Validate face data structure
                if len(face) > 4:
                    faceId = face[4]  # Extract the face ID
                    handle_detected_face(faceId)  # Process the detected face
                else:
                    print("Unexpected face data format:", face)
        else:
            print("No faces detected.")
            
            # Check timers for known and unknown faces
            if timeKnown and (time.time() - timeKnown) >= KNOWN_TIMESPACE:
                print("No known faces detected for a while.")
                timeKnown = None  # Reset the timer

    except Exception as e:
        print(f"Error during face detection: {e}")
    
    time.sleep(1)  # Wait for 1 second before the next detection cycle
