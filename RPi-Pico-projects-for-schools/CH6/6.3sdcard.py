from machine import I2C, Pin, SPI
from sdcard import SDCard
import uos
import time
from icm20948 import ICM20948

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

# Variables for tracking changes
old_x, old_y, old_z = None, None, None
start_time = time.ticks_ms()

print("Logging accelerometer data...")

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

        time.sleep(0.1)  # Log 10 readings per second

    except Exception as e:
        print(f"Error: {e}")
        break