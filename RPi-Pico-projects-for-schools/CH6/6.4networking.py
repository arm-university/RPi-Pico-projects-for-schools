from machine import I2C, Pin, SPI
from sdcard import SDCard
import uos
import time
from icm20948 import ICM20948
import network
import socket

# Wi-Fi Configuration
SSID = "Your_SSID"
PASSWORD = "Your_PASSWORD"

# Initialize I2C and Sensor
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
imu = ICM20948(i2c)

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
    FN = "/sd/accel_data.csv"
    with open(FN, "w") as f:
        f.write("Time,X,Y,Z\n")
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

# Variables for tracking changes
old_x, old_y, old_z = None, None, None
start_time = time.ticks_ms()

print("Logging accelerometer data and serving it over HTTP...")

# Main Loop
while True:
    try:
        # Read current accelerometer data
        new_x, new_y, new_z = imu.read_accelerometer()

        # Calculate timestamp in seconds
        elapsed_time = time.ticks_diff(time.ticks_ms(), start_time) / 1000.0

        # Skip the comparison for the first reading (edge case)
        if old_x is None:
            old_x, old_y, old_z = new_x, new_y, new_z
            print(f"Initial Reading @ {elapsed_time:.2f}s: X={new_x:.2f}, Y={new_y:.2f}, Z={new_z:.2f}")
        else:
            # Calculate differences
            diff_x = abs(new_x - old_x)
            diff_y = abs(new_y - old_y)
            diff_z = abs(new_z - old_z)

            # Only log significant changes
            threshold = 0.1
            if diff_x > threshold or diff_y > threshold or diff_z > threshold:
                print(f"Change @ {elapsed_time:.2f}s: X={new_x:.2f}, Y={new_y:.2f}, Z={new_z:.2f}")

                # Write data to SD card
                with open(FN, "a") as f:
                    f.write(f"{elapsed_time:.2f},{new_x:.2f},{new_y:.2f},{new_z:.2f}\n")

                # Update old readings
                old_x, old_y, old_z = new_x, new_y, new_z

        # Serve data over HTTP
        client, addr = server.accept()
        print("Client connected from", addr)
        request = client.recv(1024)
        request = str(request)
        if "/data" in request:
            with open(FN, "r") as f:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
                response += f.read()
            client.send(response)
        else:
            client.send("HTTP/1.1 404 Not Found\r\n\r\n")
        client.close()

        time.sleep(0.1)  # Log 10 readings per second

    except Exception as e:
        print(f"Error: {e}")
        break
