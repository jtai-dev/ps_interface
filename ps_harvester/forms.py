from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from pathlib import Path

from ps_harvester.models import HarvestFile, HarvestProcess, HarvestEntrySpeech


def validate_json(uploaded_file):

    if Path(uploaded_file.name).suffix == ".json":
        return uploaded_file
    else:
        raise ValidationError(
            _("%(filename)s is not a JSON file."),
            code="notJSON",
            params={"filename": uploaded_file.name},
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            raise ValidationError("Please select at least one file to upload.")
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class HarvestFilesForm(forms.Form):
    files = MultipleFileField(validators=(validate_json,))

    def save(self, process):
        harvest_files = []

        for file in self.cleaned_data["files"]:
            harvest_file = HarvestFile.objects.create(process=process, filepath=file)
            harvest_files.append(harvest_file)

        return harvest_files


class ProcessNotesForm(forms.ModelForm):
    class Meta:
        model = HarvestProcess
        fields = ("notes",)


class EntryNotesForm(forms.ModelForm):
    class Meta:
        model = HarvestEntrySpeech
        fields = ("notes",)
