from machine import I2C, Pin
from icm20948 import ICM20948

# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20))

# Initialize the ICM20948 sensor
imu = ICM20948(i2c_addr=0x68, i2c_bus=i2c)
print("ICM20948 initialized successfully.")