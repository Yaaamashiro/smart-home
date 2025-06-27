import subprocess
from pathlib import Path
from webapp.models import InfraredSignal

def register_ir(name):
    try:
        base_dir = Path(__file__).resolve().parent.parent
        script_path = base_dir / 'receive_ir.py'

        result = subprocess.check_output(['python3', str(script_path)], stderr=subprocess.STDOUT)
        content = result.decode('utf-8').strip()

        InfraredSignal.objects.update_or_create(name=name, defaults={'content': content})

        return {'status': 'ok'}

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': e.output.decode('utf-8')}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
