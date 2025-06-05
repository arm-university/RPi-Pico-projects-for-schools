import time
from breakout_bme68x import BreakoutBME68X
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
import network
import urequests
from math import floor

# Wi-Fi and ThingSpeak Configuration
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"
THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Initialize Display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
BLUE = display.create_pen(0, 0, 255)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Initialize I2C and BME Sensor
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
bme680 = BreakoutBME68X(i2c)

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
display.set_pen(BLUE)
display.clear()
display.text("Connecting to Wi-Fi...", 10, 10, scale=2)
display.update()

while not wlan.isconnected():
    try:
        wlan.connect(SSID, PASSWORD)
        time.sleep(1)
    except:
        pass

display.set_pen(GREEN)
display.clear()
display.text("Wi-Fi Connected!", 10, 10, scale=2)
display.update()

# Main Loop for Sensor Data and ThingSpeak Upload
while True:
    # Read Sensor Data
    temperature, pressure, humidity, gas, _, _, _ = bme680.read()
    temp = str(temperature)
    pres = str(floor(pressure))
    hum = str(floor(humidity))
    gas = str(floor(gas))
    
    # Display Data on Explorer Board
    display.set_pen(WHITE)
    display.clear()
    display.text(f"Temp: {temp}C", 10, 20, scale=2)
    display.text(f"Press: {pres}Pa", 10, 40, scale=2)
    display.text(f"Hum: {hum}%", 10, 60, scale=2)
    display.text(f"Gas: {gas}", 10, 80, scale=2)
    display.update()
    
    # Prepare and Send Data to ThingSpeak
    url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temp}&field2={pres}&field3={hum}&field4={gas}"
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            display.set_pen(GREEN)
            display.text("Upload Success!", 10, 100, scale=2)
        else:
            display.set_pen(RED)
            display.text("Upload Failed!", 10, 100, scale=2)
        display.update()
        response.close()
    except Exception as e:
        display.set_pen(RED)
        display.text(f"Error: {e}", 10, 100, scale=1)
        display.update()
    
    time.sleep(15)  # Wait before the next upload
