from machine import Pin, I2C #So we can access the I2C card
import time
try:
    from ppwhttp import * #Try and get the ppwhttp library
    picowireless.init() #Initialise the wireless board for the LED
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")


## SET I2C bus - using pico pins 20/21
sda=machine.Pin(20) 
scl=machine.Pin(21)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000) #0 is the id of the board (first),
                                                #freq is max frequency for the clock.

## Enable LSM303D accelerator at I2C addr 0x1Dh (29 in base 10)
config=bytearray(1)    
config[0]=39+8# 47 #0010 1111 - 6.25Hz, BDU mode 1, enable x y and z accels
i2c.writeto_mem(29, 32, config) #Write to device 29 in register 32
time.sleep(0.1)


def get_axis(reg): ## 40 - X , 42 - Y , 44 - Z
    high=bytearray(1) #High byte
    low=bytearray(1) #Low byte
    i2c.readfrom_mem_into(29, reg, low) #Read the data
    i2c.readfrom_mem_into(29, reg+1, high) #into the two bytes
    res = high[0] * 256 + low[0] #Join the two bytes together
    if (res<16384): #Deal with the 2's complement
        result = res/16384.0
    elif (res>=16384 and res<49152):
        result = (32768-res)/16384.0
    else:
        result = (res-65536)/16384.0
    return result #Return the reading

while True:
    try:
        x = get_axis(40) #Get the X acceleration
        y = get_axis(42) #Get the Y acceleration
        z = get_axis(44) #Get the Z acceleration
        set_led(0, 255, 0) #Make the WiFi LED green
        print(x,y,z) #Output the accelerations
        time.sleep(0.10) #10 checks a second
    except: #If something goes wrong
        set_led(255,0,0) #Make the LED red
        print("failure") #Output an error
        break #Jump out of the loop and stop execution
