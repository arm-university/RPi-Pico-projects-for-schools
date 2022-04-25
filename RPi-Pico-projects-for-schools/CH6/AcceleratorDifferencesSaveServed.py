from machine import Pin, I2C #So we can access the I2c card
import time
try:
    from ppwhttp import * #Try and get the ppwhttp library
    picowireless.init() #Initialise the wireless board for the LED
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")
try:
    import sdcard #Try and get the sdcard library
except ImportError: #If something goes wrong, output an error.
    raise RuntimeError("Cannot find sdcard. Have you copied ppwhttp.py to your Pico?")
import uos

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

FN = "/sd/data.csv"
with open(FN, "w") as f: # Write header  
    f.write("Timepoint,X,Y,Z\r\n")  


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

#Initialise variables for use in change calculations and timepoints
x,y,z,oldx,oldy,oldz,timepoint = None,None,None,None,None,None,None
minute = 0
second = 0
tenth = 0
 

start_wifi() #Start the WiFi connection
print(get_ip_address()) #Output the IP address
time.sleep(1) #Write it down quickly!
server_sock = start_server() #Start the server

#Handle the request for file - based on the ppwhttp handle http request
def handle_file_request(server_sock,timeout=5000): 
    t_start = time.ticks_ms() #Start counting in case of timeouts

    client_sock = picowireless.avail_server(server_sock) #Get the client socket
    if client_sock in [server_sock, 255, -1]:
        return False

    print("Client connected!")

    avail_length = picowireless.avail_data(client_sock) #Check if there is a request
    if avail_length == 0:
        picowireless.client_stop(client_sock)
        return False #If not, exit

    request = b"" #Create a binary string for request

    while len(request) < avail_length:
        data = picowireless.get_data_buf(client_sock) #get the data request
        request += data
        if time.ticks_ms() - t_start > timeout: #Check for timeouts
            print("Client timed out getting data!")
            picowireless.client_stop(client_sock)
            return False

    request = request.decode("utf-8") #Decode the request
    if "GET /data" in request: #We only want to respond if the request is for the
        #data url (eg:http://123.456.7.8/data) everything else gets a 501
        #Data requested
        print("SENDING...")
        filesize = uos.stat(FN)[6] #You have to tell the client how much data to expect
        #response = "HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: text/html\r\n\r\n".format(filesize)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        #Send the header
        picowireless.send_data(client_sock, response)
        with open(FN, "r") as f: #We will send a line at a time
            for index, line in enumerate(f): #But due to size cannot load all into memory at once
                picowireless.send_data(client_sock,line) #Send a line
                #print("Sent",index) #this can be commented out to speed things up
        picowireless.client_stop(client_sock) #Close the socket
        print("Success!")
        return True
    else: #For other URLs (including the fav icon auto request) return 501 not implemented
        response = "HTTP/1.1 501 Not Implemented\r\nContent-Length: 19\r\n\r\n501 Not Implemented"
        picowireless.send_data(client_sock, response)
        picowireless.client_stop(client_sock)
        print(response)


while True:
    #Handle the accelerometer
    try:
        newx = get_axis(40) #Get the X acceleration
        newy = get_axis(42) #Get the Y acceleration
        newz = get_axis(44) #Get the Z acceleration
        set_led(0, 255, 0) #Make the WiFi LED green
        #Make the time point a string
        timepoint = str(minute)+":"+str(second)+"."+str(tenth)
        if oldx != None: #Skip the first round
            x = newx - oldx #Calculate
            y = newy - oldy # the
            z = newz - oldz #differences
            with open(FN, "a") as f: # Write header
                f.write(timepoint+","+str(x)+","+str(y)+","+str(z)+"\r\n")
        #Add a tenth of a second and convert to seconds/minutes
        oldx,oldy,oldz = newx,newy,newz #Prep xyz for next time
        tenth += 1
        if tenth == 10:
            tenth = 0
            second += 1
        if second == 60:
            second = 0
            minute += 1
        print(timepoint,x,y,z) #Output the accelerations
        time.sleep(0.10) #10 checks a second
    except: #If something goes wrong
        set_led(255,0,0) #Make the LED red
        print("failure") #Output an error
        break #Jump out of the loop and stop execution
    #Check for http (file) requests
    handle_file_request(server_sock)
