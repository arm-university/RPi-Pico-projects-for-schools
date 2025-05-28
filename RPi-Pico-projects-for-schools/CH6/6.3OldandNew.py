from machine import I2C, Pin, SPI
from time import sleep, ticks_ms, ticks_diff
from icm20948 import ICM20948

# Initialize I2C and sensor
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
imu = ICM20948(i2c)

# Variables for tracking changes
old_x, old_y, old_z = None, None, None  # Initialize previous readings
time_start = ticks_ms()  # Start time for timestamp calculation

# Main Loop
while True:
    # Read current accelerometer data
    new_x, new_y, new_z = imu.read_accelerometer()

    # Calculate timestamp in seconds
    elapsed_time = ticks_diff(ticks_ms(), time_start) / 1000.0

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
        threshold = 0.1  # Adjust as needed to filter noise
        if diff_x > threshold or diff_y > threshold or diff_z > threshold:
            print(f"Change @ {elapsed_time:.2f}s: X={new_x:.2f}, Y={new_y:.2f}, Z={new_z:.2f}")

            # Update old readings
            old_x, old_y, old_z = new_x, new_y, new_z

    sleep(0.1)  # 10 readings per second
    
    
    