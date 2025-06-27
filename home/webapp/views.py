import json
from .models import InfraredSignal
from django.shortcuts import render
from django.http import JsonResponse
from webapp.utils.send_ir import send_ir
from webapp.utils.register_ir import register_ir

def index(request):
    signals = InfraredSignal.objects.all()
    return render(request, 'webapp/index.html', {'signals': signals})

def post_register_ir(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        result = register_ir(name)
        return JsonResponse(result)

def post_send_ir(request):
    try:
        data = json.loads(request.body)
        name = data.get('id')
        result = send_ir(name)
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
