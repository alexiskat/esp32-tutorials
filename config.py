WIFI_SSID = 'weebaws-ssid'
WIFI_PASSWORD = 'weebaws-password'

WEBHOOK_URL = 'https://api.thingspeak.com/update?api_key=WEEBAWS&field1={temperature}&field2={humidity}'
BUTTON_ID = 'micropython1'

LED1_PIN = 2  # -> D4
# Disable below for main_07...py and enable for the rest
# LED2_PIN = 16  # -> D0

DEBUG_PIN = 5  # -> D1

FAHRENHEIT = False
DHT22_PIN = 4  # -> D2

LOG_INTERVAL = 60  # set in seconda

DISPLAY_SCL_PIN = 0  # D3
DISPLAY_SDA_PIN = 12  # D6
