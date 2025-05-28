import time
import struct
from machine import I2C

class ICM20948:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self._bank = -1

        # Check WHO_AM_I register
        if self._read_byte(0x00) != 0xEA:
            raise RuntimeError("ICM20948 not found at address 0x68")

        # Reset and initialize
        self._write_byte(0x06, 0x80)  # Reset
        time.sleep(0.1)
        self._write_byte(0x06, 0x01)  # Set clock
        self._write_byte(0x07, 0x00)  # Enable all axes

    def _read_byte(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _write_byte(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def read_accelerometer(self):
        data = self.i2c.readfrom_mem(self.addr, 0x2D, 6)
        x, y, z = struct.unpack(">hhh", data)
        return x / 16384, y / 16384, z / 16384

    def read_gyroscope(self):
        data = self.i2c.readfrom_mem(self.addr, 0x33, 6)
        x, y, z = struct.unpack(">hhh", data)
        return x / 131, y / 131, z / 131
