import time
import network
import urequests
from machine import PWM, Pin

SSID = 
PASSWORD = 

network.WLAN(network.STA_IF).active(True)
network.WLAN(network.STA_IF).connect(SSID, PASSWORD)

while True:
    if network.WLAN(network.STA_IF).status() < 0 or network.WLAN(network.STA_IF).status() >= 3:
        break
    time.sleep(1)