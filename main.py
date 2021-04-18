
import sys
import dht
import time
import config
import ssd1306
import network
import machine
import urequests


def get_temperature_and_humidity():
    print('Invoking temp and humidity reading')
    dht22 = dht.DHT22(machine.Pin(config.DHT22_PIN))
    dht22.measure()
    temperature = dht22.temperature()
    if config.FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32
    print('Temprature:', temperature)
    print('Humidity  :{0}'.format(dht22.humidity))
    return temperature, dht22.humidity()


def show_error():
    led = machine.Pin(config.LED1_PIN, machine.Pin.OUT)
    for i in range(3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    led.on()


def connect_wifi():
    # disable Access  Point on controller
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi")
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print("Network Config:", sta_if.ifconfig())


def log_data(temp, humidity):
    print('Invoking log webhook')
    url = config.WEBHOOK_URL.format(
        temperature=temp,
        humidity=humidity,
    )
    r = urequests.get(url)
    if r is not None and r.status_code < 400:
        print("Webhook Invoked")
    else:
        print("Webhook Failed")
        raise RuntimeError('Webhook Failed')
    print(r.status_code)
    print(r.text)


def deep_sleep():
    print('Going to deep sleep for {seconds} seconds ...'.format(
        seconds=config.LOG_INTERVAL
    ))
    rtc = machine.RTC()
    # setup how the alarm will work
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # setup the time interval
    rtc.alarm(rtc.ALARM0, config.LOG_INTERVAL * 1000)
    machine.deepsleep()  # the wake will happen by the alarm resetting the device


def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print("Debug Mode detected")
        return True
    return False


def display_temperature_and_humidity(temperature, humidity):
    i2c = machine.I2C(scl=machine.Pin(config.DISPLAY_SCL_PIN),
                      sda=machine.Pin(config.DISPLAY_SDA_PIN))
    if 60 not in i2c.scan():
        raise RuntimeError('Cannot find display.')

    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.fill(0)

    display.text('{:^16s}'.format('Temperature:'), 0, 0)
    display.text('{:^16s}'.format(str(temperature) +
                                  ('F' if config.FAHRENHEIT else 'C')), 0, 16)

    display.text('{:^16s}'.format('Humidity:'), 0, 32)
    display.text('{:^16s}'.format(str(humidity) + '%'), 0, 48)

    display.show()
    time.sleep(5)
    display.poweroff()


def run():
    try:
        # if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        connect_wifi()
        t, h = get_temperature_and_humidity()
        log_data(t, h)
        display_temperature_and_humidity(t, h)
    except Exception as exc:
        sys.print_exception(exc)
        show_error()
    if not is_debug():
        deep_sleep()


# call the run fuction
run()
