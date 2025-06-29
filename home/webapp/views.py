import json
from .models import InfraredSignal, Lock
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webapp.utils.send_ir import send_ir
from webapp.utils.register_ir import register_ir

def index(request):
    signals = InfraredSignal.objects.all()
    lock = Lock.objects.first()

    return render(
        request,
        'webapp/index.html',
        {
            'signals': signals,
            'lock': lock,
        }
    )

@csrf_exempt
def post_register_ir(request):
    name = request.POST.get('name')
    result = register_ir(name)
    return JsonResponse(result)

@csrf_exempt
def post_send_ir(request):
    try:
        data = json.loads(request.body)
        name = data.get('id')
        result = send_ir(name)
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

@csrf_exempt
def post_toggle_lock(request):
    lock, _ = Lock.objects.get_or_create(id=1, defaults={'is_opened': True})
    lock.is_opened = not lock.is_opened
    lock.save()
    return redirect('index')
