from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from django.views.generic import View, ListView, UpdateView, FormView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect

from ps_harvester.fileharvest.process import main as file_harvest, HarvestError

from ps_harvester.forms import (
    HarvestFilesForm,
    ProcessNotesForm,
    EntryNotesForm,
)

from ps_harvester.models import (
    HarvestProcess,
    HarvestEntrySpeech,
    HarvestStatus,
)


class HarvestProcessList(LoginRequiredMixin, ListView):

    login_url = reverse_lazy("ps_auth:login")

    template_name = "ps_harvester/process-list.html"
    context_object_name = "processes_with_entries"
    model = HarvestProcess
    paginate_by = 10
    ordering = ("-created",)

    def get_queryset(self):
        processes = super().get_queryset()
        entries_for_review = HarvestEntrySpeech.objects.filter(review=True)
        entries_resolved = HarvestEntrySpeech.objects.filter(review=False)

        queryset = processes.prefetch_related(
            Prefetch("harvestentryspeech_set", to_attr="all_entries"),
            Prefetch(
                "harvestentryspeech_set",
                queryset=entries_for_review.order_by("entry_id"),
                to_attr="entries_for_review",
            ),
            Prefetch(
                "harvestentryspeech_set",
                queryset=entries_resolved.order_by("entry_id"),
                to_attr="entries_resolved",
            ),
        )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        page_obj = context.get("page_obj")

        if page_obj is not None:
            paginator = page_obj.paginator
            context["custom_elided_page_range"] = paginator.get_elided_page_range(
                page_obj.number, on_each_side=2
            )

        return context


class HarvestProcessDetail(DetailView):

    template_name = "ps_harvester/process-detail.html"
    model = HarvestProcess

    def get_queryset(self):
        processes = super().get_queryset()
        entries_resolved = HarvestEntrySpeech.objects.filter(review=False)

        queryset = processes.prefetch_related(
            Prefetch(
                "harvestentryspeech_set",
                to_attr="entries_resolved",
                queryset=entries_resolved.order_by("entry_id"),
            )
        )
        return queryset


class DeleteHarvestProcess(PermissionRequiredMixin, View):
    permission_required = [
        "ps_harvester.delete_harvestprocess",
    ]

    def post(self, request, pk):
        p = HarvestProcess.objects.get(process_id=pk)
        p.delete()
        return JsonResponse({"redirect_url": reverse("ps_harvester:process_list")})


class EditProcessNotes(PermissionRequiredMixin, UpdateView):

    permission_required = [
        "ps_harvester.change_harvestprocess",
    ]

    template_name = "ps_harvester/process-list.html"
    context_object_name = "edit_process_notes"
    model = HarvestProcess
    form_class = ProcessNotesForm

    def get(self, request, pk):
        return JsonResponse({"notes": self.get_object().notes})

    def post(self, request, pk):
        form = self.get_form()
        form.instance = self.get_object()
        form.instance.notes = request.POST.get("notes")

        if form.is_valid():
            self.object = form.save()
            return JsonResponse({"msg": "Update notes successful!"})
        else:
            error_msg = "".join(form.errors.get("notes"))
            return JsonResponse({"msg": error_msg})


class EditEntryNotes(PermissionRequiredMixin, UpdateView):

    permission_required = [
        "ps_harvester.change_harvestentryspeech",
    ]

    template_name = "ps_harvester/process-list.html"
    context_object_name = "edit_entry_notes"
    model = HarvestEntrySpeech
    form_class = EntryNotesForm

    def get(self, request, pk):
        return JsonResponse({"notes": self.get_object().notes})

    def post(self, request, pk):
        form = self.get_form()
        form.instance = self.get_object()
        form.instance.notes = request.POST.get("notes")

        if form.is_valid():
            self.object = form.save()
            return JsonResponse({"msg": "Update notes successful!"})
        else:
            error_msg = "".join(form.errors.get("notes"))
            return JsonResponse({"msg": error_msg})


class ResolveHarvestEntry(PermissionRequiredMixin, View):

    permission_required = [
        "ps_harvester.change_harvestentryspeech",
    ]

    def post(self, request, pk):
        e = HarvestEntrySpeech.objects.get(entry_id=pk)
        e.resolve()
        process_status = e.process.refresh_status()
        entries_count = HarvestEntrySpeech.objects.filter(process=e.process).count()

        return JsonResponse(
            {
                "process_status": process_status,
                "entries_count": entries_count,
            }
        )


class UnresolveHarvestEntry(PermissionRequiredMixin, View):

    permission_required = [
        "ps_harvester.change_harvestentryspeech",
    ]

    def post(self, request, pk):
        e = HarvestEntrySpeech.objects.get(entry_id=pk)
        e.unresolve()
        process_status = e.process.refresh_status()
        return JsonResponse({})


class DeleteHarvestEntry(PermissionRequiredMixin, View):

    permission_required = [
        "ps_harvester.delete_harvestentryspeech",
    ]

    def post(self, request, pk):
        e = HarvestEntrySpeech.objects.get(entry_id=pk)
        e.delete()
        process_status = e.process.refresh_status()
        entries_count = HarvestEntrySpeech.objects.filter(process=e.process).count()

        return JsonResponse(
            {
                "process_status": process_status,
                "entries_count": entries_count,
            }
        )


class FileHarvester(PermissionRequiredMixin, FormView):

    permission_required = [
        "ps_harvester.add_harvestentryspeech",
        "ps_harvester.add_harvestprocess",
    ]

    template_name = "ps_harvester/file-harvest.html"
    form_class = HarvestFilesForm
    success_url = reverse_lazy("ps_harvester:file_harvest")

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            process = HarvestProcess.objects.create()

            harvest_files = form.save(process=process)
            file_contents = [hf.file_content for hf in harvest_files]
            try:
                speech_candidate_to_harvest = file_harvest(file_contents)

                for speech_candidate_id, harvest in speech_candidate_to_harvest.items():
                    HarvestEntrySpeech.objects.create(
                        process=process,
                        candidate_id=harvest["candidate_id"],
                        speech_candidate_id=speech_candidate_id,
                        review=harvest["review"],
                        review_message=harvest["review_message"],
                    )

            except HarvestError as e:
                process.error_msg = str(e)
                process.status = HarvestStatus.objects.get(status_name="ERROR")

            process.refresh_status()

            return HttpResponseRedirect(reverse("ps_harvester:process_list"))

        else:
            returned_context = (
                {"form_upload_error": form.errors["files"]}
                if "files" in form.errors
                else {}
            )

            return render(
                request,
                "ps_harvester/file-harvest.html",
                context={"form": HarvestFilesForm()} | returned_context,
            )
