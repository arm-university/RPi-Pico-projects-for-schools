from machine import I2C, Pin

i2c = I2C(0, scl=Pin(21), sda=Pin(20))
print("Scanning I2C bus...")
devices = i2c.scan()
print("Found devices:", [hex(addr) for addr in devices])
