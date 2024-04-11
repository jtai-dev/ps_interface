from django import forms
from ps_pvsadmin import models


class SpeechUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Speech
        fields = (
            "speechtype",
            "title",
            "speechdate",
            "location",
            "speechtext",
            "url",
        )
