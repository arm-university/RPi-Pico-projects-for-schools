import time  # To enable delays
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_RGB332

# Initialize display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type = PEN_RGB332)
WIDTH, HEIGHT = display.get_bounds()  # Get screen dimensions

BLUE = display.create_pen(0, 0, 255)
WHITE = display.create_pen(255, 255, 255)

# Define the text to display
quote = (
    "1925 IBM Manual: All parts should go together without forcing. "
    "You must remember that the parts you are reassembling were disassembled by you. "
    "Therefore, if you can't get them together again, there must be a reason."
)

while True:  
    # Set pen to blue and clear the screen
    display.set_pen(BLUE) # Blue
    display.clear()  # Clear the screen with the current pen color

    # Set pen to white and display the text
    display.set_pen(WHITE)  # White
    display.text(quote, 20, 20, 200, scale=2)  # Display text at (20, 20) with scale 2
    # Update the screen to apply changes
    display.update()
    # Short delay to control loop speed
    time.sleep(0.1)  # 100ms delay

