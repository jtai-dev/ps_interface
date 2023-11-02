

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch

from django.views.generic import (View,
                                  ListView,
                                  UpdateView,
                                  FormView,
                                  )

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


from ps_harvester.file_harvest import (main as file_harvest,
                                       HarvestError)

from ps_harvester.forms import (HarvestFilesForm,
                                ProcessNotesForm,
                                EntryNotesForm,
                                )

from ps_harvester.models import (HarvestProcess,
                                 HarvestEntrySpeech,
                                 HarvestStatus,
                                 )


class HarvestProcessView(LoginRequiredMixin, ListView):

    login_url = reverse_lazy('ps_auth:login')

    template_name = 'ps_harvester/harvester.html'
    context_object_name = 'processes_with_entries'
    model = HarvestProcess
    paginate_by = 15

    def get_queryset(self):
        process_by_newest = HarvestProcess.objects.order_by('-created')
        entries_for_review = HarvestEntrySpeech.objects.filter(review=True)
        entries_resolved = HarvestEntrySpeech.objects.filter(review=False)

        queryset = process_by_newest.prefetch_related(
            Prefetch('harvestentryspeech_set', to_attr='all_entries'),
            Prefetch('harvestentryspeech_set',
                     queryset=entries_for_review, to_attr='entries_for_review'),
            Prefetch('harvestentryspeech_set',
                     queryset=entries_resolved, to_attr='entries_resolved'),
        )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        paginator = page_obj.paginator
        context['custom_elided_page_range'] = paginator.get_elided_page_range(
            page_obj.number, on_each_side=2)

        return context


class EditProcessNotes(LoginRequiredMixin, UpdateView):

    login_url = reverse_lazy('ps_auth:login')

    template_name = 'ps_harvester/harvester.html'
    context_object_name = 'edit_process_notes'
    model = HarvestProcess
    form_class = ProcessNotesForm

    def get(self, request, pk):
        return JsonResponse({'notes': self.get_object().notes})

    def post(self, request, pk):
        form = self.get_form()
        form.instance = self.get_object()
        form.instance.notes = request.POST.get('notes')

        if form.is_valid():
            self.object = form.save()
            return JsonResponse({'msg': "Update notes successful!"})
        else:
            error_msg = "".join(form.errors.get('notes'))
            return JsonResponse({'msg': error_msg})


class EditEntryNotes(LoginRequiredMixin, UpdateView):

    login_url = reverse_lazy('ps_auth:login')

    template_name = 'ps_harvester/harvester.html'
    context_object_name = 'edit_entry_notes'
    model = HarvestEntrySpeech
    form_class = EntryNotesForm

    def get(self, request, pk):
        return JsonResponse({'notes': self.get_object().notes})

    def post(self, request, pk):
        form = self.get_form()
        form.instance = self.get_object()
        form.instance.notes = request.POST.get('notes')

        if form.is_valid():
            self.object = form.save()
            return JsonResponse({'msg': "Update notes successful!"})
        else:
            error_msg = "".join(form.errors.get('notes'))
            return JsonResponse({'msg': error_msg})


class ResolveHarvestEntry(PermissionRequiredMixin, View):

    permission_required = ["ps_harvester.change_harvestentryspeech",]

    def post(self, request, pk):
        e = HarvestEntrySpeech.objects.get(entry_id=pk)
        e.resolve()
        process_status = e.process.refresh_status()
        return JsonResponse({'process_status': process_status})


class DeleteHarvestEntry(PermissionRequiredMixin, View):

    permission_required = ["ps_harvester.delete_harvestentryspeech",]

    def post(self, request, pk):
        e = HarvestEntrySpeech.objects.get(entry_id=pk)
        e.delete()
        process_status = e.process.refresh_status()
        return JsonResponse({'process_status': process_status})


class FileHarvester(PermissionRequiredMixin, FormView):

    permission_required = ["ps_harvester.add_harvestentryspeech", 
                           "ps_harvester.add_harvestprocess",]

    template_name = "ps_harvester/file_harvester.html"
    form_class = HarvestFilesForm
    success_url = reverse_lazy('ps_harvester:file_harvester')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
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

            except HarvestError as e:
                process.error_msg = str(e)
                process.status = HarvestStatus.objects.get(status_name='ERROR')

            process.refresh_status()

            return HttpResponseRedirect(reverse('ps_harvester:harvester'))

        else:
            returned_context = {
                'form_upload_error': form.errors['files']} if 'files' in form.errors else {}
            
            return render(request, 'ps_harvester/file_harvester.html',
                          context={'form': HarvestFilesForm()} | returned_context)


def web_harvester(request):
    return render(request, 'ps_harvester/web_harvester.html')
