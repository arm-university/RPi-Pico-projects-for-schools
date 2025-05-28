import time
from breakout_bme68x import BreakoutBME68X
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS, Buzzer
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)# Set up the hardware
i2c = PimoroniI2C(20,21)
bme = BreakoutBME68X(i2c, address=0x76)

BLUE = display.create_pen(0, 0, 255)# set up pens
WHITE = display.create_pen(255, 255, 255)

BUZZER = Buzzer(0)  # Create a buzzer on pin 0
GASTRIGGER = 45000  # Threshold for gas resistance warning

def warning(): # Warning function
    """Produce a warning tone using the buzzer."""
    for _ in range(10):  # 10 beeps
        BUZZER.set_tone(600)  # 600 Hz tone
        time.sleep(0.1)
        BUZZER.set_tone(-1)  # No sound
        time.sleep(0.1)
while True: # Main loop
    temperature, pressure, humidity, gas_resistance, _, _, _ = bme.read()# Read sensor values as tuple
    display.set_pen(BLUE)
    display.clear()
    display.set_pen(WHITE)
    print("Temperature (°C):", temperature)
    print("Pressure (Pa):", pressure)
    print("Humidity (%):", humidity)
    print("gas_resistance (ohms): ",gas_resistance)
    
    if gas_resistance < GASTRIGGER:    # Check gas resistance threshold
        warning()   
    time.sleep(1.0)  # Sleep for 1 second



