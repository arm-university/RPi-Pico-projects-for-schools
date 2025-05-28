from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
from machine import ADC, Pin
from time import sleep

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
WIDTH, HEIGHT = display.get_bounds()

# Set up audio pin
audio_pin = Pin(0, Pin.OUT)

# Buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Potentiometer
pot = ADC(Pin(26))

# Map a value from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# File
FILENAME = "socialmedia.csv"

# STATES
START = 0
WAITING = 1
ENTERING = 2

period = 0  # Incrementing period to keep track of recordings
MAXCOUNTER = 60 * 15  # 15 minutes
state = START  # Start state

# Social Media State
social_media = [['YouTube', False, 20, 20],
                ['Facebook', False, 20, 200],
                ['Pinterest', False, 140, 20]]

def display_text(text, x, y, color=(0, 0, 0), size=2):
    display.set_pen(display.create_pen(*color))
    display.text(text, x, y, WIDTH, size)
    display.update()

# Main Loop
while True:
    if state == START:
        counter = 0
        display.set_pen(display.create_pen(255, 255, 255))
        display.clear()
        display_text('Press Y to start', 60, 100)
        
        if button_y.is_pressed:
            state = WAITING
        
        with open(FILENAME, "w") as f:
            f.write('period,YouTube,Facebook,Pinterest,time_spent\n')
        
        sleep(0.2)
    
    elif state == WAITING:
        display.set_pen(display.create_pen(255, 255, 255))
        display.clear()
        display_text('Waiting...', 60, 100)
        display_text(f"{MAXCOUNTER - counter} s", 60, 120)
        counter += 1
        sleep(1)
        
        if counter == MAXCOUNTER:
            counter = 0
            state = ENTERING
    
    elif state == ENTERING:
        display.set_pen(display.create_pen(255, 255, 255))
        display.clear()
        
        for i, sm in enumerate(social_media):
            color = (0, 255, 0) if sm[1] else (255, 0, 0)
            display_text(sm[0], sm[2], sm[3], color)
        
        # Button Controls
        if button_a.is_pressed:
            social_media[0][1] = not social_media[0][1]
        if button_b.is_pressed:
            social_media[1][1] = not social_media[1][1]
        if button_x.is_pressed:
            social_media[2][1] = not social_media[2][1]
        
        sleep(0.2)
        
        # Potentiometer Input
        pot_value = pot.read_u16()
        pot_mapped = map_value(pot_value, 0, 65535, 0, 15)
        display_text(f"{pot_mapped} minutes", 60, 150, (0, 0, 255))
        
        # Confirmation
        display_text("Confirm (Y)", 140, 200)
        if button_y.is_pressed:
            period += 1
            with open(FILENAME, "a") as f:
                f.write(f"{period},{social_media[0][1]},{social_media[1][1]},{social_media[2][1]},{pot_mapped}\n")
            state = WAITING
    
    display.update()
    print(state)
