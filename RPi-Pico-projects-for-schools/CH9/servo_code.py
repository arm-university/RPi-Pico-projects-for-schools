from machine import Pin, PWM
from utime import sleep_ms

MID = 1500000
MIN = 1000000
MAX = 2000000
SERVOPIN = 15
SERVOFREQ = 50

servo = PWM(Pin(SERVOPIN))
servo.freq(SERVOFREQ)
servo.duty_ns(MID) #Initialize to middle position
sleep(1)

while True:
    servo.duty_ns(MIN) #Move to minimum
    sleep(1)
    servo.duty_ns(MID) #Back to middle
    sleep(1)
    servo.duty_ns(MAX) #Move to maximum
