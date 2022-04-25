from machine import Pin, PWM
from utime import sleep_ms

buzzer = PWM(Pin(15))
buzzer.freq(500)
buzzer.duty_u16(1000)
sleep(1)
buzzer.duty_u16(0)
