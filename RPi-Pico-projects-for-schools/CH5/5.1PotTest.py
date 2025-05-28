from machine import Pin, ADC
from time import sleep  # For delays


# Set up potentiometer on ADC pin 26
pot = ADC(Pin(26))


# Main Loop
while True:
    # Read potentiometer value (0–65535), scale it to 0–100
    pot_value = pot.read_u16()
    mapped_value = int(pot_value /100)
    print(f"Potentiometer: {pot_value} -> Mapped: {mapped_value}")
    
    
    sleep(0.1)  # Pause for 0.1 seconds before repeating
    
    
    
    
    