from django.shortcuts import render
from ps_harvester.models import HarvestProcess


def harvester(request):
    processes = HarvestProcess.objects.order_by('-created')
    processes_with_entries = processes.prefetch_related(
        'harvestentryspeech_set')
    return render(request, 'ps_harvester/harvester.html', context={'processes': processes_with_entries})


def file_harvester(request):
    return render(request, 'ps_harvester/file_harvester.html')


def web_harvester(request):
    return render(request, 'ps_harvester/web_harvester.html')
