from machine import I2C #Gain access to the I2C port
from vl53l1x import VL53L1X #Import the ToF library
import time
#Set up the i2c connection
sda=machine.Pin(20) 
scl=machine.Pin(21)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)

distance = VL53L1X(i2c) #Start the ToF sensor
while True:
    print("range: mm ", distance.read()) #Output the distance reading
    time.sleep(0.05) #Pause