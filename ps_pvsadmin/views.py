from typing import Any

from django.db.models.query import QuerySet
from django.urls import reverse_lazy


from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
    RedirectView,
)

from ps_pvsadmin.models import (
    Speech,
    SpeechType,
    SpeechCandidate,
)

from ps_pvsadmin.forms import SpeechUpdateForm
from decouple import config


TESTING = config("TESTING", cast=bool)


class RedirectToPVSAdminMixin(RedirectView):
    url = config("PVSADMIN_URL")


class RedirectToCandidateMixin(RedirectToPVSAdminMixin):
    url = RedirectToPVSAdminMixin.url + config("PVSADMIN_CD_URL")


class RedirectToStatementsMixin(RedirectToPVSAdminMixin):
    url = RedirectToCandidateMixin.url + config("PVSADMIN_PS_URL")


class SpeechCandidateView(DetailView, RedirectToStatementsMixin):
    template_name = "ps_pvsadmin/ps_statements.html"
    model = SpeechCandidate
    context_object_name = "speech_candidate"
    pk_url_kwarg = "speech_candidate_id"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if TESTING is False:
            return super(RedirectToStatementsMixin, self).get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        selected = self.get_object()
        candidate = selected.candidate

        # Show all available speechtypes
        speechtypes = sorted(
            SpeechType.objects.all(), key=lambda x: int(x.speechtype_id)
        )

        related_speech_candidates = SpeechCandidate.objects.filter(
            speech=selected.speech
        ).exclude(pk=selected.pk)

        context.update(
            {
                "candidate_id": candidate.candidate_id,
                "candidate_name": f"{candidate.firstname} {candidate.middlename} {candidate.lastname}",
                "speech": selected.speech,
                "speech_form": SpeechUpdateForm(instance=selected.speech),
                "speechtypes": speechtypes,
                "related": related_speech_candidates,
            },
        )

        return context

    def get_queryset(self) -> QuerySet[Any]:
        speech_candidate = super().get_queryset()
        speech_and_candidate = speech_candidate.select_related("speech", "candidate")
        return speech_and_candidate


class UpdateSpeechView(UpdateView, RedirectToPVSAdminMixin):
    template_name = "ps_pvsadmin/ps_statements.html"
    model = Speech
    form_class = SpeechUpdateForm
    context_object_name = "speech_form"
    pk_url_kwarg = "speech_id"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if TESTING is False:
            return super(RedirectToPVSAdminMixin, self).get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        self.object = form.save()
        return JsonResponse({"msg": f"Speech ID: {self.object.pk} updated!"})

    def form_invalid(self, form) -> HttpResponse:
        error_msg = "; ".join(form.errors)
        return JsonResponse({"msg": f"{error_msg} required."}, status=400)


class DeleteSpeechCandidateView(DeleteView, RedirectToPVSAdminMixin):
    model = SpeechCandidate
    template_name = "ps_pvsadmin/ps_statements.html"
    success_url = reverse_lazy("ps_harvester:harvester")
    pk_url_kwarg = "speech_candidate_id"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if TESTING is False:
            return super(RedirectToPVSAdminMixin, self).get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class DeleteSpeechView(DeleteView, RedirectToPVSAdminMixin):
    model = Speech
    template_name = "ps_pvsadmin/ps_statements.html"
    success_url = reverse_lazy("ps_harvester:harvester")
    pk_url_kwarg = "speech_id"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if TESTING is False:
            return super(RedirectToPVSAdminMixin, self).get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
