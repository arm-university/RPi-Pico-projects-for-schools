from machine import I2C #Gain access to the I2C port
try:
    from vl53l1x import VL53L1X #Import the ToF library
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find vl53l1x. Have you copied it to your Pico?")
try:
    from ppwhttp import * #Try and get the ppwhttp library
    picowireless.init() #Initialise the wireless board for the LED
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")
import time
try:
    import sdcard #Try and get the sdcard library
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find sdcard. Have you copied sdcard.py to your Pico?")
import uos

#Set up the i2c connection
sda=machine.Pin(20) 
scl=machine.Pin(21)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
button=machine.Pin(12,machine.Pin.IN,machine.Pin.PULL_UP)


#Sort out the SD card
sck=machine.Pin(18,machine.Pin.OUT)
mosi=machine.Pin(19, machine.Pin.OUT)
miso=machine.Pin(16, machine.Pin.OUT)
sd_spi = machine.SPI(0, sck=sck, mosi=mosi,miso=miso)
cs=machine.Pin(22)
sd = sdcard.SDCard(sd_spi, cs)
uos.mount(sd, "/sd")  
print("Size: {} MB".format(sd.sectors/2048)) # to display card's capacity in MB  
print("\n=======================\n")  
print("Basic SDcard Test \n")

distance = VL53L1X(i2c) #Start the ToF sensor
#The states
READY = 0
COUNTING = 1
SAVING = 2
state = READY #0 is "ready", 1 is "dropping", 2 is "saving"

led_status = 0
try:
    while True:
        dist = distance.read()
        if state == READY: #Ready - wait for button press to start recording.
            set_led(0,0,255)
            distances = [] #List of distances to store
            if button.value() == False:
                state = COUNTING
        elif state == COUNTING: #counting - flash green fast while dropping
            if led_status:
                set_led(0,0,0)
            else: 
                set_led(0,255,0)
            led_status=not led_status
            if dist < 10:
                state = SAVING
            else:
                distances.append((time.ticks_ms(),distance.read()))
        else: #Must be SAVING
            set_led(255,0,0)
            print("Saving")
            filecount = 0
            while True:
                try: 
                    FN = "/sd/"+str(filecount)+".csv"
                    uos.stat(FN)
                    filecount += 1
                except:
                    with open(FN, "w") as f: # Write header
                        f.write("ms,distance\r\n")
                        for item in distances:
                            f.write(str(item[0])+","+str(item[1])+"\r\n")
                    state = 0
                    break
                
        #print("range: mm ", dist) #Output the distance reading
        time.sleep(0.05)
except:
    while True:
        if led_status:
            set_led(0,0,0)
        else: 
            set_led(255,0,0)
        led_status=not led_status
        time.sleep(0.5)
