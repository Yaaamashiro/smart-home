from django.shortcuts import render
from django.http import JsonResponse
from .models import InfraredSignal
import json
import subprocess
from pathlib import Path

def index(request):
    signals = InfraredSignal.objects.all()
    return render(request, 'webapp/index.html', {'signals': signals})

def register_ir(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        try:
            base_dir = Path(__file__).resolve().parent.parent
            script_path = base_dir / 'receive_ir.py'

            result = subprocess.check_output(['python3', str(script_path)])
            content = result.decode('utf-8').strip()

            from .models import InfraredSignal
            InfraredSignal.objects.update_or_create(name=name, defaults={'content': content})

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def send_ir(request):
    try:
        data = json.loads(request.body)
        ir = InfraredSignal.objects.get(id=data['id'])

        subprocess.run(['bto_advanced_USBIR_cmd', '-t', ir.content], check=True)

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})