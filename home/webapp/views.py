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
            # receive_ir.py のパスを取得
            base_dir = Path(__file__).resolve().parent.parent
            script_path = base_dir / 'receive_ir.py'

            # スクリプト実行
            result = subprocess.check_output(['python3', str(script_path)], stderr=subprocess.STDOUT)
            content = result.decode('utf-8').strip()

            # DBに保存（上書き or 新規）
            InfraredSignal.objects.update_or_create(name=name, defaults={'content': content})

            return JsonResponse({'status': 'ok'})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'status': 'error', 'message': e.output.decode('utf-8')})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


def send_ir(request):
    try:
        data = json.loads(request.body)
        name = data.get('id')  # JavaScript側から送られてくる name（例: "IR1"）

        ir = InfraredSignal.objects.get(name=name)

        subprocess.run(['bto_advanced_USBIR_cmd', '-t', ir.content], check=True)

        return JsonResponse({'status': 'ok'})

    except InfraredSignal.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f"No IR signal named '{name}' found."})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 'message': f"送信失敗: {e}"})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
