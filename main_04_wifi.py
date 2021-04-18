
import config
import network
import urequests

sta_if = network.WLAN(network.STA_IF)
sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
sta_if.isconnected()

headers = {}
headers['Content-Type'] = 'application/json'
url = 'https://maker.ifttt.com/trigger/button_pressed/with/key/dqi3f39woJZ8Wb3mrtuFma'
r = urequests.post(url, headers=headers, json={"value1": "micropython1",
                   "value2": "micropython2", "value3": "micropython3"})
r.text
r.status_code
