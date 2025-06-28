import subprocess
import time
from webapp.models import InfraredSignal

def register_ir(name):
    try:
        subprocess.call("bto_advanced_USBIR_cmd -r", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        subprocess.call("bto_advanced_USBIR_cmd -s", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = subprocess.check_output("bto_advanced_USBIR_cmd -g", shell=True)
        content = result.decode('utf-8').strip()

        InfraredSignal.objects.update_or_create(name=name, defaults={'content': content})

        return {'status': 'ok'}

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': e.output.decode('utf-8')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
