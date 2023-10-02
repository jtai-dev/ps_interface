from django.shortcuts import render
from django.http import JsonResponse
from ps_harvester.models import HarvestProcess

import json

def harvester(request):
    processes = HarvestProcess.objects.order_by('-created')
    processes_with_entries = processes.prefetch_related(
        'harvestentryspeech_set')
    return render(request, 'ps_harvester/harvester.html', context={'processes': processes_with_entries})


def file_harvester(request):
    if request.method == 'POST' and request.FILES['harvestfiles']:
        harvestfiles = request.FILES.getlist('harvestfiles')
        for file in harvestfiles:
            if file.multiple_chunks():
                json_string = "".join([chunk.decode() for chunk in file.chunks()])
            else:
                json_string = file.read()
        
        file_content = json.loads(json_string)
    
    else:
        file_content = None
       
    number_of_entries = len(file_content) if file_content else None
    return render(request, 'ps_harvester/file_harvester.html', context={'number_of_entries': number_of_entries})


def web_harvester(request):
    return render(request, 'ps_harvester/web_harvester.html')
