from django.shortcuts import render
from ps_harvester.models import HarvestProcess, HarvestEntrySpeech


def harvester(request):
    processes = HarvestProcess.objects.order_by('-created')
    entries = HarvestEntrySpeech.objects.all()
    return render(request, 'ps_harvester/harvester.html', context={'processes': processes,
                                                                   'entries': entries})


def file_harvester(request):
    return render(request, 'ps_harvester/file_harvester.html')


def web_harvester(request):
    return render(request, 'ps_harvester/web_harvester.html')
