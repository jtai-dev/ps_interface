from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch


from ps_harvester.file_harvest import (main as file_harvest,
                                       HarvestError)

from ps_harvester.forms import HarvestFilesForm
from ps_harvester.models import (HarvestProcess,
                                 HarvestEntrySpeech,
                                 HarvestStatus)

from django.views.generic import ListView

class Harvester(ListView):

    template_name = 'ps_harvester/harvester.html'
    context_object_name = 'processes_with_entries'
    model = HarvestProcess
    paginate_by = 15

    def get_queryset(self):
        entries_for_review = HarvestEntrySpeech.objects.filter(review=True)
        process_by_newest = HarvestProcess.objects.order_by('-created')

        queryset = process_by_newest.prefetch_related(
            Prefetch('harvestentryspeech_set', to_attr='all_entries'),
            Prefetch('harvestentryspeech_set',
                     queryset=entries_for_review, to_attr='entries_for_review'),
        )

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        paginator = page_obj.paginator
        context['custom_elided_page_range'] = paginator.get_elided_page_range(page_obj.number, on_each_side=2)

        return context
        

def resolve_entry(request, pk):
    e = HarvestEntrySpeech.objects.get(entry_id=pk)
    e.resolve()

    json_response = {'change_status': False}

    if not HarvestEntrySpeech.objects.filter(review=True, process=e.process):
        e.process.status = HarvestStatus.objects.get(status_name='COMPLETE')
        e.process.save()
        json_response['change_status'] = True
        json_response['status_css_class'] = 'complete-status'

    json_response['status_name'] = e.process.status.status_name

    return JsonResponse(json_response)


def delete_entry(request, pk):
    e = HarvestEntrySpeech.objects.get(entry_id=pk)
    e.remove()
    json_response = {'change_status': False}

    if (not HarvestEntrySpeech.objects.filter(review=True, process=e.process)
            and len(HarvestEntrySpeech.objects.filter(process=e.process)) > 0):
        e.process.status = HarvestStatus.objects.get(status_name='COMPLETE')
        e.process.save()
        json_response['change_status'] = True
        json_response['status_css_class'] = 'complete-status'

    elif (len(HarvestEntrySpeech.objects.filter(process=e.process)) == 0):
        e.process.status = HarvestStatus.objects.get(status_name='INVALID')
        e.process.save()
        json_response['change_status'] = True
        json_response['status_css_class'] = 'invalid-status'

    json_response['status_name'] = e.process.status.status_name

    return JsonResponse(json_response)


def file_harvester(request):

    if request.method == 'POST':
        files_form = HarvestFilesForm(request.POST, request.FILES)

        if files_form.is_valid():
            file_harvest_handler(files_form)
            return HttpResponseRedirect(reverse('ps_harvester:harvester'))
        else:
            returned_context = {
                'form_upload_error': files_form.errors['files']} if 'files' in files_form.errors else {}
            files_form = HarvestFilesForm()
    else:
        files_form = HarvestFilesForm()
        returned_context = {}

    return render(request, 'ps_harvester/file_harvester.html',
                  context={'files_form': files_form} | returned_context)


def file_harvest_handler(form):

    process = HarvestProcess.objects.create()

    harvest_files = form.save(process=process)
    file_contents = [hf.file_content for hf in harvest_files]

    try:
        speech_candidate_to_harvest = file_harvest(file_contents)

        for speech_candidate_id, harvest in speech_candidate_to_harvest.items():
            HarvestEntrySpeech.objects.create(process=process,
                                              speech_candidate_id=speech_candidate_id,
                                              review=harvest['review'],
                                              review_message=harvest['review_message'])

        if HarvestEntrySpeech.objects.filter(review=True, process=process):
            process.status = HarvestStatus.objects.get(
                status_name='PENDING REVIEW')
        elif HarvestEntrySpeech.objects.filter(process=process):
            process.status = HarvestStatus.objects.get(status_name='COMPLETE')

    except HarvestError as e:
        process.error_msg = str(e)
        process.status = HarvestStatus.objects.get(status_name='ERROR')

    process.save()


def web_harvester(request):
    return render(request, 'ps_harvester/web_harvester.html')
