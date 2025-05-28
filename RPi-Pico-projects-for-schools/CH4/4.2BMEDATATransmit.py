import network  # For Wi-Fi connection
import urequests  # For HTTP requests
import time  # For delays
from machine import Pin  # For onboard LED control
from pimoroni_i2c import PimoroniI2C
from breakout_bme68x import BreakoutBME68X
from math import floor  # For rounding down

# Wi-Fi Credentials
SSID = "YOUR SSID"
PASSWORD = "YOUR PASSWORD"

# ThingSpeak Settings
THINGSPEAK_API_KEY = "YOUR API"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Onboard LED Setup
led = Pin("LED", Pin.OUT)  # Built-in LED on Pico W

# I2C and BME68X Setup
BMEPINS = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**BMEPINS)
bme680 = BreakoutBME68X(i2c)


# Connect to Wi-Fi
def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    led.off()  # LED off while connecting
    print("Connecting to Wi-Fi...")
    
    wifi.connect(SSID, PASSWORD)
    
    while not wifi.isconnected():
        time.sleep(0.5)
        print("Attempting to connect to Wi-Fi...")
    
    print("Wi-Fi Connected!")
    print("IP Address:", wifi.ifconfig()[0])
    led.on()  # LED on when connected


# Send data to ThingSpeak
def send_to_thingspeak(temp, pres, hum, gas):
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temp}&field2={pres}&field3={hum}&field4={gas}"
        response = urequests.get(url)
        if response.status_code == 200:
            print("Data successfully sent to ThingSpeak!")
        else:
            print(f"Failed to send data. HTTP Code: {response.status_code}")
        response.close()
    except Exception as e:
        print("HTTP Request Failed:", e)


# Main Loop
connect_to_wifi()

while True:
    # Read Sensor Data
    temperature, pressure, humidity, gas, _, _, _ = bme680.read()
    temp = str(temperature)
    pres = str(floor(pressure))
    hum = str(floor(humidity))
    gas = str(floor(gas))
    
    print(f"Temp: {temp}°C, Pressure: {pres}Pa, Humidity: {hum}%, Gas: {gas}")
    
    # Send Data to ThingSpeak
    send_to_thingspeak(temp, pres, hum, gas)
    
    # Wait before next reading
    time.sleep(15)



