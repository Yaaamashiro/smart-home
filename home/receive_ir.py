import time
import subprocess

subprocess.call("bto_advanced_USBIR_cmd -r", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)
subprocess.call("bto_advanced_USBIR_cmd -s", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
result = subprocess.check_output("bto_advanced_USBIR_cmd -g", shell=True)
print(result.decode('utf-8').strip())