import time
import network
import urequests
from machine import PWM, Pin

motor = PWM(Pin(0))
motor.freq(50)

network.WLAN(network.STA_IF).active(True)
network.WLAN(network.STA_IF).connect("(SSID)", "(PASSWORD)")

while True:
    if network.WLAN(network.STA_IF).status() < 0 or network.WLAN(network.STA_IF).status() >= 3:
        break
    time.sleep(1)

last_status = "1"
motor.duty_u16(6100)

while True:
    response = urequests.get("http://(Home's IP Address):8000/get_lock_is_opened/")
    status = response.text.strip()
    response.close()
    print(status)

    if status != last_status:
        if status == "1":
            motor.duty_u16(6100)
        elif status == "0":
            motor.duty_u16(2900)
    last_status = status

    time.sleep(1)
