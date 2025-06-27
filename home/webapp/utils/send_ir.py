import subprocess
from webapp.models import InfraredSignal

def send_ir(name):
    try:
        signal = InfraredSignal.objects.get(name=name)

        subprocess.run(f"bto_advanced_USBIR_cmd -d {signal.content.strip()}", shell=True, check=True)

        return {'status': 'ok'}

    except InfraredSignal.DoesNotExist:
        return {'status': 'error', 'message': f"No IR signal named '{name}' found."}
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': f"送信失敗: {e}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
