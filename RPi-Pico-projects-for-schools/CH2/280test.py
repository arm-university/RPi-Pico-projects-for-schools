import time
from breakout_bme280 import BreakoutBME280
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(20,21)
bme = BreakoutBME280(i2c, address=0x76)
# create pens
BLUE = display.create_pen(0, 0, 255)
WHITE = display.create_pen(255, 255, 255)


while True:
    temperature, pressure, humidity = bme.read()# Read sensor values as tupple
    # Set pen to blue and clear the screen
    display.set_pen(BLUE) # Blue
    display.clear()  # Clear the screen with the current pen color

    # Set pen to white and display the text
    display.set_pen(WHITE)  # White
    display.text(f"Temperature (°C): {temperature:.2f}", 5, 20, scale=2)
    display.text(f"Pressure (°C): {pressure:.2f}", 5, 40, scale=2)
    display.text(f"Humidity (°C): {humidity:.2f}", 5, 60, scale=2)

    
    display.update() #Update the screen to apply changes
    time.sleep(0.1)  # 100ms delay


    


   