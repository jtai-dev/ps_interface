from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

from ps_pvsadmin import views

app_name = "ps_pvsadmin"


urlpatterns = [
    path(
        "ps/speech_candidate/<int:speech_candidate_id>/<int:candidate_id>",
        view=views.SpeechCandidateView.as_view(),
        name="speech_by_candidate",
    ),
    path(
        "ps/speech_candidate/<int:speech_candidate_id>/delete",
        view=views.DeleteSpeechCandidateView.as_view(),
        name="speech_candidate_delete",
    ),
    path(
        "ps/speech/<int:speech_id>/update",
        view=views.UpdateSpeechView.as_view(),
        name="speech_update",
    ),
    path(
        "ps/speech/<int:speech_id>/delete",
        view=views.DeleteSpeechView.as_view(),
        name="speech_delete",
    ),
]
