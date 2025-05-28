import time
from breakout_bme280 import BreakoutBME280
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS, Buzzer
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)# Set up the hardware
i2c = PimoroniI2C(20,21)
bme = BreakoutBME280(i2c, address=0x76)

BLUE = display.create_pen(0, 0, 255)# set up pens
WHITE = display.create_pen(255, 255, 25)
                           
BUZZER = Buzzer(0)
# Function to produce a warning tone
def warning():
    for _ in range(10):  # 10 beeps
        BUZZER.set_tone(600)  # 600 Hz
        time.sleep(0.1)  # 1/10 second
        BUZZER.set_tone(-1)  # No sound
        time.sleep(0.1)  # 1/10 second



# Constants
XPOS = 20  # X position for text
WIDTH = 200  # Width for text wrapping
GASTRIGGER = 35  # Threshold for air quality warning
FILENAME = "/environment.csv"  # File to store data

# Prepare file
with open(FILENAME, "w") as f:
    pass  # Create or clear the file

# Main loop
while True:
    # Open file for appending
    with open(FILENAME, "a") as f:
        # Clear screen
        display.set_pen(BLUE)  # White pen
        display.clear()

        # Read data from the sensor
        display.set_pen(WHITE)  # Black pen
        temperature, pressure, humidity, = bme.read()

        # Display data on screen
        display.text(f"Temperature (°C): {temperature:.2f}", 5, 20, scale=2)
        display.text(f"Pressure (hPa): {pressure:.2f}", 5, 40, scale=2)
        display.text(f"Humidity (%): {humidity:.2f}", 5, 60, scale=2)
        #display.text(f"Gas (Ohms): {gas_resistance:.2f}", 5, 80, scale=2)
        display.update()

        # Write data to the file
        file_string = f"{temperature},{pressure},{humidity}\n"
        f.write(file_string)


        # Update the screen
        display.update()

        # Trigger warning if air quality is poor
        if temperature > GASTRIGGER:
            warning()

    # Delay before the next loop iteration
    time.sleep(1.0)
