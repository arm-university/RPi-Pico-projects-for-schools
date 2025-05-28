import network  # For WiFi connection
import urequests  # For HTTP requests
import time  # For delays
from machine import Pin # For controlling the onboard LED

# Wi-Fi credentials
SSID = "Your ssid"  # Replace with your WiFi SSID
PASSWORD = "your password"  # Replace with your WiFi  Password

# HTTP Settings
HTTP_REQUEST_HOST = "http://google.com"

# Onboard LED setup
led = Pin("LED",Pin.OUT)  # Built-in LED on Pico W

# Connect to WiFi
def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    led.off()  # LED off while connecting
    print("Connecting to WiFi...")
    
    wifi.connect(SSID, PASSWORD)
    
    while not wifi.isconnected():
        time.sleep(0.5)  # Wait until connected
        print("Connecting to WiFi...")
    
    print("Connected to WiFi!")
    print("IP Address:", wifi.ifconfig()[0])
    led.on()  # LED on when connected

# Perform an HTTP GET request
def make_http_request():
    try:
        response = urequests.get(HTTP_REQUEST_HOST)
        print("HTTP Response Code:", response.status_code)
        print("Response Content:", response.text[:500])  # Show first 100 characters
        response.close()
    except Exception as e:
        print("HTTP Request Failed:", e)

# Main Program
connect_to_wifi()
make_http_request()





