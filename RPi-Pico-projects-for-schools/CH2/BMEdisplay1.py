import time
from breakout_bme68x import BreakoutBME68x
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(20,21)
bme = BreakoutBME68x(i2c, address=0x76)
# create pens
BLUE = display.create_pen(0, 0, 255)
WHITE = display.create_pen(255, 255, 255)


while True:
    temperature, pressure, humidity, gas_resistance,-,-,- = bme.read()# Read sensor values as tuple
    # Set pen to blue and clear the screen
    display.set_pen(BLUE) # Blue
    display.clear()  # Clear the screen with the current pen color

    # Set pen to white and display the text
    display.set_pen(WHITE)  # White
    print("Temperature (°C):", temperature)
    print("Pressure (Pa):", pressure)
    print("Humidity (%):", humidity)
    print("gas_resistance (ohms): ",gas_resistance)
    
    display.update() #Update the screen to apply changes
    time.sleep(0.1)  # 100ms delay


    


   