from machine import I2C, Pin, SPI
from vl53l1x import VL53L1X
from sdcard import SDCard
import uos
import time
import network
import socket

# Wi-Fi Configuration
SSID = "Tina"
PASSWORD = "Rubberduck2145"

# I2C Setup for VL53L1X
sda = Pin(20)
scl = Pin(21)
i2c = I2C(0, scl=scl, sda=sda, freq=100000)

# SPI Setup for SD Card
sck = Pin(18)
mosi = Pin(19)
miso = Pin(16)
cs = Pin(5)
spi = SPI(0, sck=sck, mosi=mosi, miso=miso)

# Initialize SD Card
try:
    print("Initializing SD card...")
    sd = SDCard(spi, cs)
    uos.mount(sd, "/sd")
    print("SD card mounted successfully!")

    # Create a new file and write the header
    FN = "/sd/distance_data.csv"
    with open(FN, "w") as f:
        f.write("ms,distance\n")
except OSError as e:
    print(f"SD card error: {e}")
    raise SystemExit()

# Wi-Fi Setup
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi!")
    print("IP Address:", wlan.ifconfig()[0])

connect_to_wifi()

# HTTP Server Setup
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)
    return s

server = start_server()

# Initialize VL53L1X Sensor
distance = VL53L1X(i2c)


# Button Setup
button = Pin(12, Pin.IN, Pin.PULL_UP)

# State Variables
READY = 0
COUNTING = 1
SAVING = 2
state = READY
led_status = False
start_time = time.ticks_ms()
distances = []

# Main Loop
print("Logging distance data and serving over HTTP...")
while True:
    try:
        dist = distance.read()

        if state == READY:  # Wait for button press to start recording
            if button.value() == 0:
                print("Starting measurement...")
                distances = []
                state = COUNTING

        elif state == COUNTING:  # Record distances until close enough
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            distances.append((elapsed_time, dist))
            print(f"{elapsed_time}ms -> Distance: {dist}mm")

            if dist < 10:  # Save if object is detected within 10mm
                state = SAVING

        elif state == SAVING:  # Save data to SD card
            print("Saving data to SD card...")
            with open(FN, "a") as f:
                for item in distances:
                    f.write(f"{item[0]},{item[1]}\n")
            state = READY

        # Handle HTTP requests
        client, addr = server.accept()
        print("Client connected from", addr)
        request = client.recv(1024).decode("utf-8")
        if "/data" in request:
            with open(FN, "r") as f:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
                response += f.read()
            client.send(response)
        else:
            client.send("HTTP/1.1 404 Not Found\r\n\r\n")
        client.close()

        time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
        break
