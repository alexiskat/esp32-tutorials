import machine
import time

led = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
while button.value():
    led.on()
    led2.off()
    time.sleep(0.5)
    led.off()
    led2.on()
    time.sleep(0.5)
led.on()
led2.on()
