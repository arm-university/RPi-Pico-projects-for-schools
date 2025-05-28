import time
from breakout_bme68x import BreakoutBME68X
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(20,21)
bme = BreakoutBME68X(i2c, address=0x76)

# set up pen
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)


# Main loop to read sensor data
while True:
    # Read sensor values as tuple
    temperature, pressure, humidity, gas_resistance, *_ = bme.read()
    
    # Print each reading
    print("Temperature (°C):", temperature)
    print("Pressure (Pa):", pressure)
    print("Humidity (%):", humidity)
    print("gas_resistance (ohms): ",gas_resistance)
    
    # Wait for 1 second before the next reading
    time.sleep(1.0)
    
    
    
    