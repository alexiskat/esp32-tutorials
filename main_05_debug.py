
import sys
import time
import config
import network
import machine
import urequests


def show_error():
    led = machine.Pin(config.LED1_PIN, machine.Pin.OUT)
    led2 = machine.Pin(config.LED2_PIN, machine.Pin.OUT)
    for i in range(3):
        led.on()
        led2.off()
        time.sleep(0.5)
        led.off()
        led2.on()
        time.sleep(0.5)
    led.on()
    led2.on()


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


def call_webhook():
    print("Invoking Webhook...")
    headers = {}
    headers['Content-Type'] = 'application/json'
    r = urequests.post(config.WEBHOOK_URL,
                       headers=headers,
                       json={"value1": config.BUTTON_ID,
                             "value2": "micropython2",
                             "value3": "micropython3"})
    if r is not None and r.status_code < 400:
        print("Webhook Invoked")
    else:
        print("Webhook Failed")
        raise RuntimeError('Webhook Failed')
    print(r.status_code)
    print(r.text)


def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print("Debug Mode detected")
        return True
    return False


def run():
    try:
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            connect_wifi()
            call_webhook()
    except Exception as exc:
        sys.print_exception(exc)
        show_error()
    if not is_debug():
        machine.deepsleep()


# call the run fuction
run()
