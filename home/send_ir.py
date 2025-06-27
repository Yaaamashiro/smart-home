import sys
import os
import django
import subprocess

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_home.settings")
django.setup()

from webapp.models import InfraredSignal

def send_ir(name):
    try:
        signal = InfraredSignal.objects.get(name=name)
        cmd = f"bto_advanced_USBIR_cmd -d '{signal.content.strip()}'"
        subprocess.call(cmd, shell=True)
    except InfraredSignal.DoesNotExist:
        print(f"Error: No IR signal with name '{name}' found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_ir.py <IR_NAME>")
        sys.exit(1)
    send_ir(sys.argv[1])
