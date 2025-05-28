from machine import I2C, Pin
from time import sleep
from icm20948 import ICM20948

# Initialize I2C and sensor
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
imu = ICM20948(i2c)

while True:
    ax, ay, az = imu.read_accelerometer()
    gx, gy, gz = imu.read_gyroscope()

    print(f"Accel: X={ax:.2f}, Y={ay:.2f}, Z={az:.2f}")
    print(f"Gyro: X={gx:.2f}, Y={gy:.2f}, Z={gz:.2f}")

    sleep(0.5)
