
from django.db import models


class HarvestStatus(models.Model):
    # Names:
    # 1) COMPLETE
    # 2) INVALID
    # 3) PENDING REVIEW
    # 4) ERROR
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.status_id}-{self.status_name}"


class HarvestProcessManager(models.Manager):
    pass


class HarvestProcess(models.Model):

    process_id = models.BigAutoField(primary_key=True)
    status = models.ForeignKey(
        HarvestStatus, default=2, on_delete=models.PROTECT)
    notes = models.TextField(null=True, default="")
    error_msg = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def refresh_status(self):

        if self.status.status_name != 'ERROR':
            if self.harvestentryspeech_set:
                if not self.harvestentryspeech_set.filter(review=True):
                    self.status = HarvestStatus.objects.get(
                        status_name='COMPLETE')
                else:
                    self.status = HarvestStatus.objects.get(
                        status_name='PENDING REVIEW')
            else:
                self.status = HarvestStatus.objects.get(status_name='INCOMPLETE')

        self.save()

        return self.status.status_name


class HarvestFile(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    filepath = models.FileField('uploads/harvest/')
    process = models.ForeignKey(HarvestProcess, on_delete=models.CASCADE)
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def file_content(self) -> str:
        if self.filepath.multiple_chunks():
            file_bytes_decoded = "".join([chunk.decode()
                                          for chunk in self.filepath.chunks()])
            self.filepath.delete()
            return file_bytes_decoded

        else:
            file_bytes = self.filepath.read()
            self.filepath.delete()
            return file_bytes.decode()


class HarvestWebDirect(models.Model):
    web_id = models.BigAutoField(primary_key=True)
    web_address = models.URLField()
    process = models.ForeignKey(HarvestProcess, on_delete=models.CASCADE)
    collected_timestamp = models.DateTimeField(auto_now_add=True)


class HarvestEntrySpeech(models.Model):
    entry_id = models.BigAutoField(primary_key=True)

    # Identifier for each statements entry on VoteSmart's Admin
    speech_candidate_id = models.BigIntegerField(editable=False)
    process = models.ForeignKey(
        HarvestProcess, on_delete=models.CASCADE, editable=False)
    review = models.BooleanField(default=False)
    review_message = models.TextField(null=True)
    notes = models.TextField(null=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def delete(self, admin=False, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def resolve(self):
        self.review = False
        self.review_message = ""
        self.save()

    @property
    def admin_url(self):
        return f"https://admin.votesmart.org/loadCandidateSpeechDetail.do?candidateSpeechId={self.speech_candidate_id}"
