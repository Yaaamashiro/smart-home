print("11001100")
'''
import time
import subprocess

subprocess.call("bto_advanced_USBIR_cmd -r", shell=True)
time.sleep(3)
subprocess.call("bto_advanced_USBIR_cmd -s", shell=True)
result = subprocess.check_output("bto_advanced_USBIR_cmd -g", shell=True)
print(result.decode('utf-8').strip())
'''