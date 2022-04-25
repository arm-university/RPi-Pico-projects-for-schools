import time #For the loop delay
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE #The BME Breakout
from pimoroni_i2c import PimoroniI2C #The I2C library
import picoexplorer as explorer #Allow access to the Pico Explorer base
from math import floor #Allow us to round down (no round() function in this MicroPython)

def warning(): #Produce a warning tone
    for i in range(10): #10 beeps
        explorer.set_tone(600) #600 hz
        time.sleep(0.1) #1/10 second
        explorer.set_tone(-1) #no sound
        time.sleep(0.1) #1/10 second

PINS_PICO_EXPLORER = {"sda": 20, "scl": 21} #The pins used for I2C on the Explorer

i2c = PimoroniI2C(**PINS_PICO_EXPLORER) #Setup I2C
bme = BreakoutBME68X(i2c) #Start the BME

width = explorer.get_width() #Get access to the height
height = explorer.get_height() #and width to setup the buffer

display_buffer = bytearray(width * height * 2)  #Create the buffer for the screen
explorer.init(display_buffer) #Initialise the explorer (and screen)
explorer.set_audio_pin(0) #Connect the audio

XPOS = 20 #XPosition of the text
WIDTH = 200 #Width of the text
GASTRIGGER = 45000 #When you want the warning to sound

FILENAME = "environment.csv" #The filename to store data in
f = open(FILENAME, "w") #Open the file for writing (to empty it)
f.close() #Close the file

while True: #Repeat forever
    f = open(FILENAME, "a") #Open the file for appending

    explorer.set_pen(255, 255, 255) #Set a white pen
    explorer.clear() #Clear the screen

    explorer.set_pen(0, 0, 0) #Set a black pen
    temperature, pressure, humidity, gas, _, _, _ = bme.read() #Read the BME as a tuple
    explorer.text("Temp: "+str(temperature)+"C",XPOS,20,WIDTH) #Write the temperature
    explorer.text("Pres: "+str(floor(pressure))+"Pa",XPOS,40,WIDTH) #Write the pressure
    explorer.text("Hum : "+str(floor(humidity))+"%",XPOS,60,WIDTH) #Write the humidity
    explorer.text("Qual: "+str(floor(gas))+" Ohms",XPOS,80,WIDTH) #Write the air quality
    #Build up the string to write (too many concatenations seem to not work!)
    fileString = str(temperature)+','+str(pressure)+','+str(humidity)+','+str(gas)
    fileString = fileString+'\n' #Add a new line (like pressing ENTER)
    f.write(fileString) #Write the data to file
    explorer.update() #Update the screen
    if (gas < GASTRIGGER): #Check against the trigger
        warning() #Trigger the warning
    f.close() #Close the file
    time.sleep(1.0) #Sleep for 1 second




    