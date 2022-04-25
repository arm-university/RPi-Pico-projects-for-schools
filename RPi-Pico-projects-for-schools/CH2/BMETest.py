import time #For the loop delay
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE #The BME Breakout
from pimoroni_i2c import PimoroniI2C #The I2C library

PINS_PICO_EXPLORER = {"sda": 20, "scl": 21} #The pins used for I2C on the Explorer

i2c = PimoroniI2C(**PINS_PICO_EXPLORER) #Setup I2C
bme = BreakoutBME68X(i2c) #Start the BME

while True:
    temperature, pressure, humidity, gas, _, _, _ = bme.read() #Read the BME as a tuple
    print("Temp (c):",temperature) #Output the temperature
    print("Pressure (Pa):",pressure) #Output the pressure
    print("Humidity (%):",humidity) #Output the humidity
    print("Gas (Ohms):",gas) #Output the air quality
    time.sleep(1.0) #Sleep for 1 second