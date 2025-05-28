from machine import Pin, ADC
from time import sleep  # For delays
from pimoroni import Button

# Set up buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Set up potentiometer on ADC pin 26
pot = ADC(Pin(26))

# Map a value from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# Main Loop
while True:
    # Read potentiometer value (0–65535), scale it to 0–100
    pot_value = pot.read_u16()
    mapped_value = map_value(pot_value, 0, 65535, 0, 100)
    print(f"Potentiometer: {pot_value} -> Mapped: {mapped_value}")
    
    # Button Inputs
    if button_a.is_pressed:
        print("Button A Pressed")
    if button_b.is_pressed:
        print("Button B Pressed")
    if button_x.is_pressed:
        print("Button X Pressed")
    if button_y.is_pressed:
        print("Button Y Pressed")
    
    sleep(0.1)  # Pause for 0.1 seconds before repeating


